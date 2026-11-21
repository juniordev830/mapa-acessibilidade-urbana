'Priorize percursos a pé com base em rampas, travessias e condições observadas das calçadas.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def textos(items):
    if not isinstance(items, list):
        raise ValueError("Use uma lista de textos.")
    return [texto(item) for item in items]


from urllib.parse import urlencode


MODOS = {"carro": "driving", "a-pe": "walking", "bicicleta": "bicycling", "onibus": "transit"}


def _url(acao, parametros):
    url = "https://www.google.com/maps/" + acao + "?" + urlencode({"api": 1, **parametros})
    if len(url) > 2048:
        raise ValueError("O endereço gerado ultrapassa o limite do Google Maps.")
    return url


def rota(origem, destino, modo="carro", paradas=(), evitar_pedagios=False):
    pontos = [texto(parada) for parada in paradas]
    if len(pontos) > 3 or any("|" in parada for parada in pontos):
        raise ValueError("Use até 3 paradas por link e evite o caractere |.")
    if modo not in MODOS:
        raise ValueError(f"Modo desconhecido: {modo}")
    params = {"origin": texto(origem), "destination": texto(destino), "travelmode": MODOS[modo]}
    if pontos:
        params["waypoints"] = "|".join(pontos)
    if evitar_pedagios:
        params["avoid"] = "tolls"
    return _url("dir/", params)


def busca(local):
    return _url("search/", {"query": texto(local)})


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    registros = data.get("percursos")
    if not isinstance(registros, list) or len(registros) > 30 or any(
        not isinstance(item, dict) for item in registros
    ):
        raise ValueError("Informe até 30 percursos como objetos.")
    origem, destino = texto(data["origem"]), texto(data["destino"])
    percursos = []
    nomes = set()
    for item in registros:
        nome = texto(item["nome"])
        if nome.casefold() in nomes:
            raise ValueError(f"Percurso repetido: {nome}.")
        nomes.add(nome.casefold())
        barreiras_registradas = item.get("barreiras")
        if not isinstance(barreiras_registradas, list) or len(barreiras_registradas) > 200 or any(
            not isinstance(bar, dict) for bar in barreiras_registradas
        ):
            raise ValueError("Informe até 200 barreiras como objetos por percurso.")
        barreiras = []
        for bar in barreiras_registradas:
            if type(bar["impeditiva"]) is not bool:
                raise ValueError("impeditiva precisa ser verdadeiro ou falso.")
            barreiras.append({"local": texto(bar["local"]), "tipo": texto(bar["tipo"]),
                              "impeditiva": bar["impeditiva"], "google_maps": busca(bar["local"])})
        percursos.append({"nome": nome, "barreiras": barreiras,
                          "impeditivas": sum(b["impeditiva"] for b in barreiras),
                          "google_maps": rota(origem, destino, "a-pe", textos(item["paradas"]))})
    percursos.sort(key=lambda item: (item["impeditivas"], len(item["barreiras"]), item["nome"]))
    return {"percursos": percursos,
            "menos_barreiras_registradas": percursos[0]["nome"] if percursos else None}


import argparse
from contextlib import nullcontext
import sys
from relatorio_csv import escrever_csv
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--csv", action="store_true", help="Exportar as barreiras observadas em cada percurso em CSV")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open(encoding="utf-8-sig")
        with entrada as source:
            data = json.load(
                source,
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.csv:
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
