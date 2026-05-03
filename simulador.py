import random

QUESTOES = [
    {
        "pergunta": "Quanto é 2 + 2?",
        "alternativas": ["3", "4", "5", "6"],
        "correta": "4"
    },
    {
        "pergunta": "Capital do Brasil?",
        "alternativas": ["RJ", "SP", "Brasília", "BH"],
        "correta": "Brasília"
    }
]

def gerar_questao():
    return random.choice(QUESTOES)