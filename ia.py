def gerar_plano(resumo):
    prompt = f"""
    Um aluno tem o seguinte desempenho:

    {resumo}

    Gere um plano de estudo simples e direto para melhorar.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content