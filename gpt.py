from gpt4all import GPT4All

model = GPT4All("GPT4All-Community/DeepSeek-R1-Distill-Llama-8B-GGUF")

class Chatbot:
    def __init__(self, user_input):
        self.user_input = user_input
        self.session = {}
        self.model = model
        self.active_session = None

    def create_session(self):
        session = self.model.chat_session()
        session_name = f"session_{len(self.session) + 1}"
        self.session[session_name] = session
        
    def select_session(self, session_name):
        self.active_session = self.session[session_name]
        
    def list_sessions(self):
        return list(self.session.keys())
    
    def chat(self, input):
        with self.active_session:
            return self.model.generate(input)