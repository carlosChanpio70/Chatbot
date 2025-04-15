from nicegui import ui
from chatbot import Chatbot
#Carlos Alexandre Camarino Terra, Eduardo Toledo França
#DentalBot


# Add custom CSS to disable scrolling on the page
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
    with ui.scroll_area().classes('w-full h-3/4 border bg-gray-400') as chat_scroll:
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