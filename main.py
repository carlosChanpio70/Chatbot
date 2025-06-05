import asyncio
from nicegui import ui
from ai import SessionManager


class SideMenu:
    def __init__(self, chatbot, chat_container):
        self.chatbot = chatbot
        self.chat_container = chat_container
        self.chat_sessions = []
        self.chat_displays = {}
        self.chat_buttons = {}  # Novo: dicionário para guardar os botões
        with ui.column().classes('w-64 h-screen bg-white shadow-lg justify-start items-stretch'):
            ui.label('DentalBot').classes('text-xl font-bold p-4 border-b')
            ui.button('Novo Chat', icon='add', on_click=self.new_chat).classes(
                'w-full justify-start')
            self.buttons_column = ui.column()

    def select_chat(self, session_name):
        self.chatbot.select_session(session_name)
        for display in self.chat_displays.values():
            display.hide()
        self.chat_displays[session_name].show()

    def new_chat(self):
        session_name = self.chatbot.create_session()
        self.chat_sessions.append(session_name)
        with self.buttons_column:
            with ui.row().classes('w-full items-center') as row:
                btn_chat = ui.button(session_name, on_click=lambda s=session_name: self.select_chat(s)).classes(
                    'flex-1 justify-start text-left').props('rounded outlined dense')
                btn_del = ui.button(icon='delete', color='red', on_click=lambda s=session_name: self.deletar_chat(
                    s)).props('flat round dense')
                # Salva o row (linha de botões) para fácil deleção
                self.chat_buttons[session_name] = row
        self.chat_displays[session_name] = ChatDisplay(
            self.chat_container, self.chatbot, session=session_name)
        self.select_chat(session_name)

    def deletar_chat(self, session_name):
        # Remove da lista de sessões e do dicionário de displays
        if session_name in self.chat_sessions:
            self.chat_sessions.remove(session_name)
            # Remove o display do chat
            self.chat_displays[session_name].hide()
            del self.chat_displays[session_name]
            # Remove os botões da interface
            self.chat_buttons[session_name].delete()
            del self.chat_buttons[session_name]
            self.chatbot.delete_session(session_name)
        if self.chat_sessions:
            self.select_chat(self.chat_sessions[-1])
        else:
            self.new_chat()


class ChatDisplay:
    def __init__(self, container, chatbot, session=None):
        with container:
            self.root = ui.column().classes('w-full')
            with self.root:
                ui.label(f'Chat: {session}').classes(
                    'text-2xl font-bold text-center p-4 border-b border-gray-300 shadow-sm')
                with ui.card().classes('w-full h-[80vh] flex flex-col shadow-lg mb-8 bg-gray-200'):
                    with ui.scroll_area().classes('flex-1 w-full border') as chat_scroll:
                        chat = ui.markdown().classes('w-full')
                    with ui.row().classes("w-full p-2"):
                        input_box = ui.input().props('rounded outlined dense').classes("flex-1")

                        async def send():
                            user_input = input_box.value
                            if not user_input or user_input.strip() == '':
                                return
                            # Executa chatbot.chat em thread para não travar a interface
                            loop = asyncio.get_event_loop()
                            result = await loop.run_in_executor(None, chatbot.chat, user_input)
                            with ui.teleport(f'#c{chat.id}'):
                                ui.chat_message(
                                    f"{user_input}", name="Usuário", sent=True).classes('w-full')
                                ui.chat_message(
                                    f"{result}", name="DentalBot", avatar="https://robohash.org/ui").classes('w-full')
                            chat_scroll.scroll_to(percent=100)
                            input_box.value = ''

                        input_box.on('keydown.enter', send)
                        ui.button(icon='send', on_click=send)

    def hide(self):
        self.root.set_visibility(False)

    def show(self):
        self.root.set_visibility(True)


chatbot = SessionManager()
with ui.row().classes('w-full h-screen'):
    menu = SideMenu(chatbot, None)
    chat_container = ui.column().classes('flex-1 h-screen justify-end items-center')
    menu.chat_container = chat_container
    menu.new_chat()

ui.run(host='127.1.1.1', port=8080, title='DentalBot')
