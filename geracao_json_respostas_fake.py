import json
import random
from datetime import datetime, timedelta

usuarios = ["dlemes", "lcoltri", "amendes"]
question_ids = list(range(4, 26))
data_respostas = []

hoje = datetime.now().strftime("%d/%m/%Y")

# Gabarito simplificado com base nas perguntas criadas
gabarito = {
    4: "a", 5: "c", 6: "b", 7: "c", 8: "b", 9: "c", 10: "b", 11: "b", 12: "c", 13: "a",
    14: "c", 15: "b", 16: "b", 17: "b", 18: "a", 19: "b", 20: "a", 21: "a", 22: "a", 
    23: "c", 24: "a", 25: "a"
}

# Função para gerar horário aleatório entre 12h e 15h
def gerar_datahora():
    hora = random.randint(12, 15)
    minuto = random.randint(0, 59)
    return f"{hoje} {hora:02}:{minuto:02}"

# Geração por usuário
for usuario in usuarios:
    num_respostas = random.randint(8, 10)
    perguntas_sorteadas = random.sample(question_ids, num_respostas)

    for qid in perguntas_sorteadas:
        tentativa = 1
        acertou = False
        while not acertou:
            if tentativa <= random.randint(1, 2):  # até 3 tentativas erradas
                alternativas = ["a", "b", "c", "d"]
                alternativas.remove(gabarito[qid])  # remove a correta para errar
                resposta = random.choice(alternativas)
            else:
                resposta = gabarito[qid]  # acerta

            data_respostas.append({
                "question_id": qid,
                "alternativa_escolhida": resposta,
                "datahora": gerar_datahora(),
                "usuario": usuario,
                "nro_tentativa": tentativa
            })

            if resposta == gabarito[qid]:
                acertou = True
            else:
                tentativa += 1

# Salvar o arquivo JSON
with open("answers.json", "w") as f:
    json.dump(data_respostas, f, indent=2)

print("Arquivo answers.json gerado com sucesso!")