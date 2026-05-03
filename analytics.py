def calcular_desempenho(dados):
    resumo = {}

    for materia, correta in dados:
        if materia not in resumo:
            resumo[materia] = {"total": 0, "acertos": 0}

        resumo[materia]["total"] += 1
        resumo[materia]["acertos"] += correta

    for materia in resumo:
        total = resumo[materia]["total"]
        acertos = resumo[materia]["acertos"]
        resumo[materia]["taxa"] = acertos / total if total > 0 else 0

    return resumo


def sugerir_materia(resumo):
    pior = None
    menor = 1

    for materia, dados in resumo.items():
        if dados["taxa"] < menor:
            menor = dados["taxa"]
            pior = materia

    return pior