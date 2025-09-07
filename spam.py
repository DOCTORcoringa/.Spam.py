from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Input
from textual.containers import Grid
from textual.reactive import reactive
from textual import work
from datetime import datetime
import re
import asyncio

OPTIONS = [
    ("Número Telefone", "phone", "Envia mensagens para números de telefone válidos."),
    ("Endereço de E-mail", "email", "Envia mensagens para e-mails válidos."),
    ("Spam SMS", "phone", "Envio massivo de SMS para números válidos."),
    ("Spam WhatsApp", "phone", "Envio massivo de mensagens pelo WhatsApp."),
    ("Spam Telegram", "username", "Envio de mensagens para usuários do Telegram."),
    ("Spam Facebook", "username", "Envio para perfis do Facebook."),
    ("Spam Instagram", "username", "Envio para perfis do Instagram."),
    ("Spam Twitter", "username", "Envio para perfis do Twitter."),
    ("Spam LinkedIn", "username", "Envio para perfis no LinkedIn."),
    ("Spam SMS Internacional", "phone", "Envio de SMS para números internacionais."),
    ("Envio por Fax", "phone", "Envio massivo por fax, números requeridos."),
    ("Spam Mensagem de Voz", "phone", "Envio de mensagens gravadas para números."),
    ("Spam Correio Postal", "address", "Envio de cartas para endereços físicos."),
    ("Spam Anúncios", "email", "Envio de anúncios por e-mail."),
    ("Spam via SMS Premium", "phone", "Envio para números premium."),
    ("Spam via Mensagens Diretas App", "username", "Envio por mensagens diretas em apps."),
    ("Spam via Notificações Push", "deviceToken", "Envio para dispositivos via notificações."),
    ("Reportar Spam", "report", "Relate tentativas de spam recebidas."),
]

QUANTITY = 500

def validate_input(input_type, value):
    patterns = {
        "phone": r"^[+]?[\d\s()-]{8,15}$",
        "email": r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        "username": r"^[a-zA-Z0-9._]{3,25}$",
        "address": r".{10,}",
        "deviceToken": r"^[a-fA-F0-9]{64}$",
        "report": r".{5,}",
    }
    pattern = patterns.get(input_type)
    if pattern:
        return re.match(pattern, value.strip()) is not None
    return False

class Banner(Static):
    def on_mount(self):
        self.set_interval(1, self.update_time)
        self.update_time()

    def update_time(self):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        banner = (
            "[b white]DCL[/b white] [b red]SPAM[/b red]\n\n"
            f"[red]{time_str}[/red]  [yellow]{date_str}[/yellow]\n"
        )
        self.update(banner)

class OptionButton(Button):
    def __init__(self, label: str, index: int):
        super().__init__(label, id=f"opt-{index}")
        self.index = index

class ProgressBar(Static):
    def set_progress(self, percent: int):
        size = 40
        filled = int(size * percent / 100)
        bar = "[" + "█" * filled + " " * (size - filled) + "]"
        self.update(f"[red]{bar} {percent}%[/red]")

class OptionBox(Static):
    def __init__(self, label: str, index: int):
        super().__init__(id=f"box-{index}")
        self.label = label
        self.index = index
        self.button = OptionButton(label, index)

    def compose(self) -> ComposeResult:
        yield Static(f"[b]{self.label}[/b]", style="green")
        yield self.button

class DCLSpamApp(App):
    CSS = """
    #banner {
        background: black;
        height: 5;
        content-align: center middle;
        padding-bottom: 1;
    }
    #menu {
        background: green;
        height: auto;
        padding: 1;
        border: round green;
        layout: grid;
        grid-size: 3;
        grid-gutter: 1 2;
        justify-items: center;
    }
    OptionBox {
        border: round yellow;
        height: 5;
        width: 20;
        padding: 0 1;
        content-align: center middle;
    }
    Button {
        background: #007700;
        border: none;
        padding: 1 2;
        width: 100%;
        text-align: center;
    }
    Button.-active {
        background: #004400;
        text-style: bold;
    }
    #inputbox {
        border: round green;
        padding: 1 2;
        margin: 1 0;
    }
    Input {
        border: round yellow;
        padding: 1 1;
        width: 100%;
    }
    #message {
        border: round green;
        padding: 1 2;
        margin-top: 1;
        min-height: 5;
    }
    #progressbar {
        height: 3;
        padding: 0 2;
        margin-top: 1;
        width: 100%;
    }
    """

    selected_index = reactive(-1)
    error_message = reactive("")
    info_message = reactive("")
    user_input = reactive("")
    in_progress = reactive(False)

    def compose(self) -> ComposeResult:
        yield Banner(id="banner")
        yield Grid(id="menu")
        for i, (label, _, _) in enumerate(OPTIONS):
            yield OptionBox(label, i)
        yield Static("", id="info")
        with Static(id="inputbox"):
            yield Static("[b yellow]Valor para a escolha selecionada:[/b yellow]\n")
            yield Input(placeholder="Digite aqui e pressione Enter...", id="input", disabled=True)
        yield ProgressBar(id="progressbar")
        yield Static("", id="message")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.in_progress:
            return

        if event.button.id and event.button.id.startswith("opt-"):
            idx = int(event.button.id.split("-")[1])
            self.select_option(idx)

    def select_option(self, idx):
        self.selected_index = idx
        self.error_message = ""
        self.info_message = f"{OPTIONS[idx][2]}"
        self.user_input = ""
        input_w = self.query_one("#input")
        input_w.value = ""
        input_w.disabled = False
        input_w.focus()
        for btn in self.query("#menu OptionBox Button"):
            btn.remove_class("-active")
        self.query_one(f"#opt-{idx}").add_class("-active")
        self.query_one("#info").update(f"[b green]{self.info_message}[/b green]")
        self.query_one("#message").update("")
        self.query_one("#progressbar").update("")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.in_progress or self.selected_index < 0:
            return
        val = event.value.strip()
        input_type = OPTIONS[self.selected_index][1]
        if not validate_input(input_type, val):
            self.error_message = f"Por favor, insira um valor válido para: {OPTIONS[self.selected_index][0]}"
            self.query_one("#message").update(f"[red]{self.error_message}[/red]")
            return

        self.error_message = ""
        self.query_one("#message").update("")
        input_w = self.query_one("#input")
        input_w.disabled = True
        self.in_progress = True

        self.set_progress(0)
        await self.run_worker(val)

    @work
    async def run_worker(self, val):
        progress = self.query_one("#progressbar")
        for i in range(101):
            progress.set_progress(i)
            await asyncio.sleep(0.05)
        self.in_progress = False
        self.finish_message(val)

    def set_progress(self, percent: int):
        progress = self.query_one("#progressbar")
        progress.set_progress(percent)

    def finish_message(self, val):
        txt = (
            f"[green]Envio concluído![/green]\n\n"
            f"A quantidade de [b yellow]500[/b yellow] itens relacionados a função '[b green]{OPTIONS[self.selected_index][0]}[/b green]' foi processada para o valor: [b white]{val}[/b white].\n\n"
            "Lembre-se: este painel é uma ferramenta auxiliar e não possui poder real de banir ou bloquear números, e-mails ou usuários.\n\n"
            "[b yellow]Créditos:[/b yellow] Doctor Coringa Lunático"
        )
        self.query_one("#message").update(txt)
        input_w = self.query_one("#input")
        input_w.disabled = False
        input_w.value = ""
        input_w.focus()

if __name__ == "__main__":
    DCLSpamApp().run()
            
