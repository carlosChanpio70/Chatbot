import nltk
from nltk.chat.util import Chat, reflections
from nltk.metrics import edit_distance

# Ensure NLTK resources are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Carlos Alexandre Camarino Terra, Eduardo Toledo França
# DentalBot

pairs = [
    [r"oi|olá|ola", ["Olá! Como posso te ajudar hoje?"]],
    [r"quem é você\?", [
        "Eu sou o DentalBot, um assistente virtual especializado em cuidados dentários."]],
    [r"o que você faz\?", [
        "Posso responder perguntas sobre saúde bucal."]],
    [r"como o que\?|de que forma\?|como você ajuda\?", [
        "Posso ajudar com informações sobre escovação, cáries, gengivite, cuidados com próteses e muito mais."]],
    [r"como devo escovar os dentes\?", [
        "Você deve escovar os dentes por pelo menos 2 minutos, 2 a 3 vezes ao dia, com uma escova macia e creme dental."]],
    [r"como evitar cáries\?", [
        "Escove os dentes regularmente, use fio dental, evite açúcar em excesso e visite seu dentista regularmente."]],
    [r"o que é uma cárie\?", [
        "A cárie é uma deterioração dos dentes causada por bactérias que produzem ácidos a partir de restos de alimentos."]],
    [r"devo usar fio dental diariamente\?", [
        "Sim! O uso diário do fio dental ajuda a remover a placa entre os dentes e prevenir gengivite e cáries."]],
    [r"o que causa o mau hálito\?", [
        "O mau hálito pode ser causado por má higiene bucal, boca seca, problemas estomacais ou infecções bucais."]],
    [r"com que frequência devo ir ao dentista\?", [
        "O ideal é visitar o dentista a cada 6 meses para uma avaliação e limpeza."]],
    [r"por que devo limpar a lingua\?", [
        "Limpar a língua evita o acúmulo de bactérias, resíduos de alimentos e células mortas."]],
    [r"como devo limpar a lingua\?", [
        "Após escovar os dentes, você pode usar um raspador lingual ou uma escova."]],
    [r"o que é gengivite\?", ["A gengivite é uma inflamação na gengiva, geralmente causada pelo acúmulo de placa bacteriana, e pode causar sangramento e inchaço."]],
    [r"escovar os dentes com força faz mal\?", [
        "Sim, escovar com muita força pode desgastar o esmalte dos dentes e machucar a gengiva. Use movimentos suaves e circulares."]],
    [r"qual é a escova de dentes ideal\?", [
        "Prefira escovas com cerdas macias e cabeça pequena, que alcançam todas as áreas da boca sem machucar."]],
    [r"posso escovar os dentes logo após comer\?", [
        "O ideal é esperar cerca de 30 minutos após as refeições para escovar os dentes, principalmente após alimentos ácidos."]],
    [r"crianças precisam usar fio dental\?", [
        "Sim, crianças devem usar fio dental assim que dois dentes estiverem encostando, para prevenir cáries entre eles."]],
    [r"o que é tártaro\?", [
        "O tártaro é a placa bacteriana endurecida que se forma nos dentes e só pode ser removido por um dentista."]],
    [r"como prevenir o tártaro\?", [
        "Escove os dentes regularmente, use fio dental e faça limpezas profissionais no dentista."]],
    [r"o que é sensibilidade nos dentes\?", [
        "A sensibilidade ocorre quando a dentina fica exposta, causando dor ao consumir alimentos ou bebidas quentes, frias ou doces."]],
    [r"como tratar dentes sensíveis\?", [
        "Use cremes dentais específicos para sensibilidade e consulte um dentista para avaliar a causa."]],
    [r"qual a importância do enxaguante bucal\?", [
        "O enxaguante bucal ajuda a reduzir bactérias, prevenir cáries e manter o hálito fresco, mas não substitui a escovação e o fio dental."]],
    [r"como escolher um creme dental\?", [
        "Escolha um creme dental com flúor, que ajuda a prevenir cáries, e que atenda às suas necessidades específicas, como sensibilidade ou clareamento."]],
    [r"o que é flúor e por que é importante\?", [
        "O flúor é um mineral que fortalece o esmalte dos dentes, ajudando a prevenir cáries e remineralizar áreas enfraquecidas."]],
    [r"como cuidar de próteses dentárias\?", [
        "Lave as próteses diariamente com uma escova macia e sabão neutro, e remova-as à noite para descansar a gengiva."]],
    [r"o que é um canal dentário\?", [
        "O tratamento de canal é um procedimento para remover a polpa infectada ou danificada do interior do dente."]],
    [r"(.*)", ["Desculpe, ainda estou aprendendo. Pode reformular sua pergunta ou tentar algo mais específico?"]],
]

reflections = {
    "eu": "você",
    "você": "eu",
    "estou": "está",
    "está": "estou",
    "fui": "foi",
    "foi": "fui",
    "meu": "seu",
    "seu": "meu",
    "meus": "seus",
    "seus": "meus",
    "minha": "sua",
    "sua": "minha",
    "minhas": "suas",
    "suas": "minhas",
    "mim": "você",
    "teu": "seu",
    "teus": "seus",
    "será": "serei",
    "serei": "será",
    "sou": "é",
    "é": "sou",
    "te": "me",
    "me": "te",
}

chatbot = Chat(pairs, reflections)


def Chatbot(user_input):
    user_input = user_input.lower()
    best_match = None
    best_score = float('inf')  # Lower scores are better for edit distance

    # Iterate through the defined patterns
    for pattern, responses in pairs:
        # Split the pattern into alternatives using '|'
        alternatives = pattern.split('|')

        for alternative in alternatives:
            # Calculate the Levenshtein distance between the user input and the pattern
            distance = edit_distance(user_input, alternative.lower())

            # Update the best match if the current distance is smaller
            if distance < best_score:
                best_match = responses[0]
                best_score = distance

    # Return the best match if the score is within a reasonable threshold
    if best_score <= 10:  # Adjust the threshold based on testing
        return best_match

    # Fallback to the original regex-based matching if no good match is found
    return chatbot.respond(user_input)

def test_chatbot():
    failed_tests = []
    for pattern, responses in pairs:
        # Use the first alternative in the pattern for testing
        test_input = pattern.split('|')[0].replace(r'\?', '?')  # Replace escaped '?' for natural input
        expected_response = responses[0]

        # Get the chatbot's response
        actual_response = Chatbot(test_input)

        # Check if the response matches the expected response
        if actual_response != expected_response:
            failed_tests.append((test_input, expected_response, actual_response))

    # Print the test results
    if not failed_tests:
        print("All tests passed!")
    else:
        print(f"{len(failed_tests)} test(s) failed:")
        for test_input, expected, actual in failed_tests:
            print(f"Input: {test_input}")
            print(f"Expected: {expected}")
            print(f"Actual: {actual}")
            print("-" * 50)
        
        
if __name__ == "__main__":
    # Run the tests when the script is executed directly
    test_chatbot()