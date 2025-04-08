import random
import nltk # type: ignore
from nltk.chat.util import Chat, reflections # type: ignore

#.\venv\Scripts\Activate.ps1

pairs = [
    [
        r"Oi|Olá|E ai|E ai\?",
        ["Olá!","Como posso ajudar?","Oi, como está?"],
    ],
    [
        r"Qual é o seu nome\?|Qual o seu nome\?",
        ["Meu nome é ChatBot.","Voce pode me chamar de ChatBot","Sou o ChatBot."],
    ],
    [
        r"(.*)\?",
        ["Desculpe, não tenho uma resposta especifíca a essa pergunta."]
    ],
]

pairs.extend([
    [r"(.*)",["Entendi. Diga-me mais.","Pode me contar mais sobre isso?","Interessante. Conte-me mais..."]],
])

reflections = {
    "eu":"você",
    "meu":"seu",
    "meus":"seus",
    "minha":"sua",
    "minhas":"suas",
    "sou":"é",
    "estou":"está",
    "fui":"foi",
    "você":"eu",
    "eu sou":"você é",
    "você está":"eu estou",
    "você estava":"eu estava",
}

chatbot= Chat(pairs, reflections)

def Chatbot(user_input):
    if user_input.lower() == "sair":
        return False
    return chatbot.respond(user_input)