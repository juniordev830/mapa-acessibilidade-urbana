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
    origem, destino = texto(data["origem"]), texto(data["destino"])
    percursos = []
    for item in data["percursos"]:
        barreiras = []
        for bar in item["barreiras"]:
            if type(bar["impeditiva"]) is not bool:
                raise ValueError("impeditiva precisa ser verdadeiro ou falso.")
            barreiras.append({"local": texto(bar["local"]), "tipo": texto(bar["tipo"]),
                              "impeditiva": bar["impeditiva"], "google_maps": busca(bar["local"])})
        percursos.append({"nome": texto(item["nome"]), "barreiras": barreiras,
                          "impeditivas": sum(b["impeditiva"] for b in barreiras),
                          "google_maps": rota(origem, destino, "a-pe", textos(item["paradas"]))})
    percursos.sort(key=lambda item: (item["impeditivas"], len(item["barreiras"]), item["nome"]))
    return {"percursos": percursos,
            "menos_barreiras_registradas": percursos[0]["nome"] if percursos else None}


import argparse
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8-sig") as source:
            data = json.load(source, object_pairs_hook=objeto_sem_campos_repetidos)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
