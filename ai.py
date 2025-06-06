from gpt4all import GPT4All
from chatbot import pairs  # Importa os pares do chatbot.py

model_name ="Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = GPT4All(model_name, device="cuda")

def build_instruction_from_pairs(pairs):
    instructions = "Você é um assistente dental chamado DentalBot, esses são alguns exemplos de perguntas e respostas que você deve usar:\n"
    for pattern, responses in pairs:
        # Usa apenas o primeiro exemplo de resposta para cada padrão
        question = pattern.replace(r'\?', '?').replace('|', '/')
        answer = responses[0]
        instructions += f"Pergunta: {question} Resposta: {answer}\n"
    return instructions

instructions = build_instruction_from_pairs(pairs)

class Chatbot:
    def __init__(self, model, session_cm, session):
        self.model = model
        self.session_cm = session_cm
        self.session = session

    def chat(self, input):
        if self.session is None:
            raise RuntimeError("No active session available.")
        response = self.model.generate(prompt=input, temp=0.6)
        return response.strip()

    def __del__(self):
        # Ensure context manager is properly exited
        if hasattr(self, 'session_cm') and self.session_cm is not None:
            self.session_cm.__exit__(None, None, None)
            self.session_cm = None
        self.session = None


class SessionManager:
    def __init__(self):
        self.model = model
        self.sessions = {}  # session_name: Chatbot instance
        self.active_session_name = None

    def create_session(self):
        session_cm = self.model.chat_session(system_prompt=instructions)
        session = session_cm.__enter__()
        chatbot = Chatbot(self.model, session_cm, session)
        session_name = f"session_{len(self.sessions) + 1}"
        self.sessions[session_name] = chatbot
        self.active_session_name = session_name
        return session_name

    def select_session(self, session_name):
        if session_name not in self.sessions:
            raise ValueError(f"Session '{session_name}' does not exist.")
        self.active_session_name = session_name

    def list_sessions(self):
        return list(self.sessions.keys())

    def delete_session(self, session_name):
        if session_name in self.sessions:
            del self.sessions[session_name]
            if self.active_session_name == session_name:
                self.active_session_name = None
        else:
            raise ValueError(f"Session '{session_name}' does not exist.")

    def chat(self, input):
        if self.active_session_name is None:
            raise RuntimeError("No active session selected.")
        chatbot = self.sessions[self.active_session_name]
        return chatbot.chat(input)