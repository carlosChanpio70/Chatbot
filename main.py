from nicegui import ui
from chatbot import Chatbot
#Carlos Alexandre Camarino Terra, Eduardo Toledo França
#DentalBot


ui.add_head_html("""
<style>
    body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden; /* Disable scrolling */
    }
</style>
""")

with ui.column().classes('w-full h-screen'):
    
    ui.label('Bem-vindo ao DentalBot') \
        .classes('text-2xl font-bold text-center p-4 border-b border-gray-300 bg-white shadow-sm')
    
    with ui.scroll_area().classes('w-full h-3/4 border bg-gray-200') as chat_scroll:
        chat = ui.markdown().classes('w-full')

    def Chat(input):
        result = Chatbot(input)
        with ui.teleport(f'#c{chat.id}'):
            ui.chat_message(f"{input}", name="Usuário",sent=True).classes('w-full')
            ui.chat_message(f"{result}", name="DentalBot",avatar="https://robohash.org/ui").classes('w-full')
        chat_scroll.scroll_to(percent=100)

    with ui.row().classes("w-full flex-auto"):
        with ui.input().props('rounded outlined dense').classes("flex-1").on('keydown.enter', lambda: Chat(input.value)) as input:
            resultado = ui.button(icon='send', on_click=lambda: Chat(input.value))

ui.run(host='127.1.1.1',port=8080, title='DentalBot')
#Carlos Alexandre Camarino Terra, Eduardo Toledo França