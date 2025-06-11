import asyncio
from nicegui import ui
from ai import SessionManager

#* Configurações iniciais da interface
ui.query('.nicegui-content').classes('p-0 gap-0')

#* Adiciona estilos personalizados para o tema escuro
ui.add_head_html("""
<style>
.background_color {
    background-color: #121212 !important;
}
.background_color2 {
    background-color: #1d1d1d !important;
}
.button_color {
    background-color: #2c2c2c !important;
}
body, .nicegui-content, .background_color, .background_color2, .button_color, .q-card, .q-btn, .q-label, .q-input, .q-field__native, .q-field__label, .q-field__control, .q-field__marginal, .q-field__append, .q-field__prepend, .q-field__bottom {
    color: #fff !important;
}
.grey_border {
    border-color: #2c2c2c !important;
    box-shadow: 0 0 0 2px #2c2c2c !important;
}
</style>
""")


class SideMenu:
    """Classe que representa o menu lateral com a lista de chats e botões para criar e deletar chats."""
    
    def __init__(self, chatbot, chat_container):
        self.chatbot = chatbot
        self.chat_container = chat_container
        self.chat_sessions = []
        self.chat_displays = {}
        self.chat_buttons = {}
        with ui.column().classes('w-64 h-screen background_color shadow-lg justify-start items-stretch'):
            ui.label('DentalBot').classes('text-xl font-bold p-4 border-b grey_border')
            
            #* Coluna para os botões de chat
            ui.button(
                'Novo Chat',
                icon='add',
                on_click=self.new_chat,
                color='#2c2c2c'
            ).classes('w-full justify-start height:42px;').props('rounded dense')
            self.buttons_column = ui.column()

    def select_chat(self, session_name):
        """Função para selecionar um chat existente e exibir seu conteúdo."""
        
        self.chatbot.select_session(session_name)
        for display in self.chat_displays.values():
            display.hide()
        self.chat_displays[session_name].show()

    def new_chat(self):
        """Função para criar um novo chat e adicionar o botão correspondente."""
        
        base_name = "Chat"
        i = 1
        while f"{base_name} {i}" in self.chat_sessions:
            i += 1
        session_name = f"{base_name} {i}"#* Gera um nome único para o novo chat
        self.chatbot.create_session(session_name)#* Cria uma nova sessão de chat
        self.chat_sessions.append(session_name)
        with self.buttons_column:#* Adiciona o botão na coluna de botões
            with ui.element('div').classes('w-full relative my-1').style('height:42px;') as row:
                btn_chat = ui.button(
                    session_name,
                    on_click=lambda s=session_name: self.select_chat(s),
                    color='#2c2c2c'
                ).classes('w-full h-full justify-start').props('rounded dense')
                btn_del = ui.button(
                    icon='delete',
                    color='red',
                    on_click=lambda s=session_name: self.deletar_chat(s)
                ).props('flat round dense').classes('absolute').style('top:4px;right:4px;width:28px;height:28px;')
                self.chat_buttons[session_name] = row
                
        #* Cria uma nova instância de ChatDisplay para mostrar o chat
        self.chat_displays[session_name] = ChatDisplay(self.chat_container, self.chatbot)
        self.select_chat(session_name)#* Seleciona o novo chat criado

    def deletar_chat(self, session_name):
        """Função para deleção de um chat"""
        
        if session_name in self.chat_sessions:
            self.chat_sessions.remove(session_name)
            # Remove o display do chat
            self.chat_displays[session_name].hide()
            del self.chat_displays[session_name]
            # Remove os botões da interface
            self.chat_buttons[session_name].delete()
            del self.chat_buttons[session_name]
            self.chatbot.delete_session(session_name)
            
        #* Se não houver mais chats, cria um novo chat
        if self.chat_sessions:
            self.select_chat(self.chat_sessions[-1])
        else:
            self.new_chat()


class ChatDisplay:
    """Classe que representa a área de chat onde as mensagens são exibidas e enviadas."""
    
    def __init__(self, container, chatbot):
        with container:
            self.root = ui.column().classes('w-full h-screen overflow-hidden background_color2')
            with self.root:
                with ui.card().classes('w-full flex-1 flex flex-col shadow-lg background_color2'):
                    
                    #* Cria a área de chat com rolagem
                    with ui.scroll_area().classes('flex-1 w-full border grey_border') as chat_scroll:
                        chat = ui.markdown().classes('w-full')
                        
                    #* Cria a área de entrada de mensagens
                    with ui.element('div').classes("w-full relative my-1"):
                        input_box = ui.input().props('rounded outlined dense').classes('w-full h-full')
                        ui.button(
                            icon='send',
                            color='gray-400',
                            on_click=lambda: asyncio.create_task(send())
                        ).props('flat round dense').classes('absolute').style('top:50%;right:4px;width:28px;height:28px;transform:translateY(-50%);')

                        async def send():
                            """Função para enviar a mensagem do usuário e receber a resposta do chatbot."""
                            
                            user_input = input_box.value
                            if not user_input or user_input.strip() == '':
                                return
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

    def hide(self):
        """Função para esconder a área de chat."""
        
        self.root.set_visibility(False)
        
    def show(self):
        """Função para mostrar a área de chat."""
        
        self.root.set_visibility(True)

#* Inicialização do chatbot e criação da interface
chatbot = SessionManager()
with ui.row().classes('w-full h-screen p-0 gap-0'):
    menu = SideMenu(chatbot, None)
    chat_container = ui.column().classes('flex-1 h-screen overflow-hidden p-0 m-0')
    menu.chat_container = chat_container
    menu.new_chat()

ui.run(host='127.1.1.1', port=8080, title='DentalBot')