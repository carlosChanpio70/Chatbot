import random
import nltk # type: ignore
from nltk.chat.util import Chat, reflections # type: ignore

#.\venv\Scripts\Activate.ps1

pairs = [
    [r"oi|olá", ["Olá! Como posso te ajudar hoje?"]],
    [r"como escovar os dentes( corretamente)\?", ["Você deve escovar os dentes por pelo menos 2 minutos, 2 a 3 vezes ao dia, com uma escova macia e creme dental."]],
    [r"o que é cárie\?", ["A cárie é uma deterioração dos dentes causada por bactérias que produzem ácidos a partir de restos de alimentos."]],
    [r"como evitar cáries\?", ["Escove os dentes regularmente, use fio dental, evite açúcar em excesso e visite seu dentista regularmente."]],
    [r"devo usar fio dental( todos os dias)\?", ["Sim! O uso diário do fio dental ajuda a remover a placa entre os dentes e prevenir gengivite e cáries."]],
    [r"o que causa mau hálito\?", ["O mau hálito pode ser causado por má higiene bucal, boca seca, problemas estomacais ou infecções bucais."]],
    [r"com que frequência devo ir ao dentista\?", ["O ideal é visitar o dentista a cada 6 meses para uma avaliação e limpeza."]],
    [r"porque devo limpar a lingua\?", ["Limpar a língua evita o acúmulo de bactérias, resíduos de alimentos e células mortas."]],
    [r"como devo ir limpar a lingua\?", ["Após escovar os dentes,você pode usar um raspador lingual ou uma escova."]],
    [r"o que é gengivite\?", ["A gengivite é uma inflamação na gengiva, geralmente causada pelo acúmulo de placa bacteriana, e pode causar sangramento e inchaço."]],
    [r"escovar os dentes com força faz mal\?", ["Sim, escovar com muita força pode desgastar o esmalte dos dentes e machucar a gengiva. Use movimentos suaves e circulares."]],
    [r"qual a escova de dentes ideal\?", ["Prefira escovas com cerdas macias e cabeça pequena, que alcançam todas as áreas da boca sem machucar."]],
    [r"posso escovar os dentes logo após comer\?", ["O ideal é esperar cerca de 30 minutos após as refeições para escovar os dentes, principalmente após alimentos ácidos."]],
    [r"crianças precisam usar fio dental\?", ["Sim, crianças devem usar fio dental assim que dois dentes estiverem encostando, para prevenir cáries entre eles."]],
    [r"(.*)", ["Desculpe, ainda estou aprendendo. Pode refazer a pergunta?"]],
]

pairs.extend([
    [r"(.*)",["Entendi. Diga-me mais.","Pode me contar mais sobre isso?","Interessante. Conte-me mais..."]],
])

reflections = {
    "eu": "você",
    "meu": "seu",
    "meus": "seus",
    "minha": "sua",
    "minhas": "suas",
    "sou": "é",
    "estou": "está",
    "fui": "foi",
    "você": "eu",
    "te": "me",
    "mim": "você",
    "seu": "meu",
    "seus": "meus",
    "sua": "minha",
    "suas": "minhas",
    "é": "sou",
    "está": "estou",
    "foi": "fui",
    "será": "serei",
}

chatbot= Chat(pairs, reflections)

def Chatbot(user_input):
    if user_input.lower() == "sair":
        return False
    return chatbot.respond(user_input)