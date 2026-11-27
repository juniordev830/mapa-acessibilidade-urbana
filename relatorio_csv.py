import csv


def celula(valor):
    """Mantém texto com aparência de fórmula como texto em planilhas."""
    if not isinstance(valor, str):
        return valor
    prefixos = ("=", "+", "-", "@", "＝", "＋", "－", "＠")
    if valor.lstrip().startswith(prefixos) or valor.startswith(("\t", "\r", "\n")):
        return "'" + valor
    return valor


def linhas(relatorio):
    for percurso in relatorio["percursos"]:
        if not percurso["barreiras"]:
            yield percurso["nome"], "", "", "", percurso["google_maps"], ""
        for barreira in percurso["barreiras"]:
            impede = "sim" if barreira["impeditiva"] else "não"
            yield (percurso["nome"], barreira["local"], barreira["tipo"], impede,
                   percurso["google_maps"], barreira["google_maps"])


def escrever_csv(relatorio, destino):
    escritor = csv.writer(destino, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
    escritor.writerow(('percurso', 'local', 'tipo', 'impeditiva', 'rota', 'mapa_barreira'))
    for linha in linhas(relatorio):
        escritor.writerow([celula(valor) for valor in linha])
