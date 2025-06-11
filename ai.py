from gpt4all import GPT4All
from chatbot import pairs  # Importa os pares do chatbot.py

#* Inicializa o modelo GPT4All com o nome do modelo e tenta carregar na GPU, se não disponível, usa a CPU
model_name ="Meta-Llama-3-8B-Instruct.Q4_0.gguf"
try:
    model = GPT4All(model_name, device="cuda")
except:
    model = GPT4All(model_name, device="cpu")

def build_instruction_from_pairs(pairs):
    """Constrói uma string de instruções a partir dos pares de perguntas e respostas do chatbot."""
    
    instructions = "Você é um assistente dental chamado DentalBot, esses são alguns exemplos de perguntas e respostas que você deve usar:\n"
    for pattern, responses in pairs:
        #* Usa apenas o primeiro exemplo de resposta para cada padrão
        question = pattern.replace(r'\?', '?').replace('|', '/')
        answer = responses[0]
        instructions += f"Pergunta: {question} Resposta: {answer}\n"
    return instructions

instructions = build_instruction_from_pairs(pairs)#* Constrói as instruções a partir dos pares

class Chatbot:
    """Classe que representa um chatbot com uma sessão de chat."""
    
    def __init__(self, model, session_cm, session):
        self.model = model
        self.session_cm = session_cm
        self.session = session

    def chat(self, input):
        """Envia uma mensagem para o chatbot e retorna a resposta."""
        
        if self.session is None:
            raise RuntimeError("No active session available.")
        response = self.model.generate(prompt=input, temp=0.6)
        return response.strip()

    def __del__(self):
        """Limpa a sessão do chatbot ao deletar a instância."""
        
        if hasattr(self, 'session_cm') and self.session_cm is not None:
            self.session_cm.__exit__(None, None, None)
            self.session_cm = None
        self.session = None


class SessionManager:
    """Classe que gerencia todas as multiplas sessões de chatbots."""
    
    def __init__(self):
        self.model = model #* Modelo do GPT4All
        self.sessions = {} #* Dicionário para armazenar as sessões de chatbots
        self.active_session_name = None #* Nome da sessão ativa

    def create_session(self, name=None):
        """Cria uma nova sessão de chatbot."""
        
        session_cm = self.model.chat_session(system_prompt=instructions)
        session = session_cm.__enter__()
        chatbot = Chatbot(self.model, session_cm, session)#* Cria uma instância do Chatbot com o modelo e a sessão
        if name== None:
            session_name = f"session_{len(self.sessions) + 1}"
        else:
            session_name = name
        self.sessions[session_name] = chatbot
        self.active_session_name = session_name
        return session_name#* Retorna o nome da sessão criada

    def select_session(self, session_name):
        """Seleciona uma sessão de chatbot ativa."""
        
        if session_name not in self.sessions:
            raise ValueError(f"Session '{session_name}' does not exist.")
        self.active_session_name = session_name

    def list_sessions(self):
        """Lista os nomes de todas as sessões de chatbot."""
        
        return list(self.sessions.keys())

    def delete_session(self, session_name):
        """Deleta uma sessão de chatbot."""
        
        if session_name in self.sessions:
            del self.sessions[session_name]
            if self.active_session_name == session_name:
                self.active_session_name = None
        else:
            raise ValueError(f"Session '{session_name}' does not exist.")

    def chat(self, input):
        """Envia uma mensagem para o chatbot na sessão ativa e retorna a resposta."""
        
        if self.active_session_name is None:
            raise RuntimeError("No active session selected.")
        chatbot = self.sessions[self.active_session_name]
        return chatbot.chat(input)