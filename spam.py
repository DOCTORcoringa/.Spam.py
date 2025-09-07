from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Input
from textual.containers import Vertical
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
    ("Reportar Spam", "report", "Relate tentativas de spam recebidas."),
]

QUANTITY = 500

def validate_input(input_type, value):
    patterns = {
        "phone": r"^[+]?[\d\s()-]{8,15}$",
        "email": r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        "username": r"^[a-zA-Z0-9._]{3,25}$",
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
            "[b green]╔══════════════════════════╗[/b green]\n"
            "[b blue]      PAINEL DCL TOOL       [/b blue]\n"
            f"[yellow] {date_str} [/yellow]   [red]{time_str}[/red]\n"
            "[b green]╚══════════════════════════╝[/b green]"
        )
        self.update(banner)

class ProgressBar(Static):
    def set_progress(self, percent: int):
        size = 20
        filled = int(size * percent / 100)
        bar = "█" * filled + "░" * (size - filled)
        self.update(f"[cyan]{bar} {percent}%[/cyan]")

class Footer(Static):
    def on_mount(self):
        self.update(
            "\n[b magenta]✦ Doctor Coringa Lunático ✦[/b magenta]\n"
            "[italic yellow]Transformando códigos em caos organizado[/italic yellow]\n"
        )

class DCLApp(App):
    CSS = """
    #banner {
        background: black;
        height: 6;
        content-align: center middle;
        padding: 1;
    }
    #menu {
        padding: 1;
        border: round green;
        height: auto;
        content-align: center middle;
    }
    Button {
        background: #005500;
        padding: 1;
        margin: 1 0;
        width: 100%;
        text-align: center;
    }
    Button.-active {
        background: #227722;
        text-style: bold;
    }
    Input {
        border: round yellow;
        padding: 1;
        width: 100%;
    }
    #info, #message {
        padding: 1;
        margin: 1 0;
        border: round blue;
    }
    #progressbar {
        margin: 1 0;
    }
    #footer {
        content-align: center middle;
        padding: 1;
    }
    """

    selected_index = reactive(-1)
    in_progress = reactive(False)

    def compose(self) -> ComposeResult:
        yield Banner(id="banner")
        with Vertical(id="menu"):
            for i, (label, _, _) in enumerate(OPTIONS):
                yield Button(label, id=f"opt-{i}")
        yield Static("[b yellow]Selecione uma opção acima.[/b yellow]", id="info")
        yield Input(placeholder="Digite o valor e pressione Enter...", id="input", disabled=True)
        yield ProgressBar(id="progressbar")
        yield Static("", id="message")
        yield Footer(id="footer")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.in_progress:
            return
        if event.button.id and event.button.id.startswith("opt-"):
            idx = int(event.button.id.split("-")[1])
            self.select_option(idx)

    def select_option(self, idx):
        self.selected_index = idx
        info = OPTIONS[idx][2]
        self.query_one("#info").update(f"[green]{info}[/green]")
        inp = self.query_one("#input")
        inp.value = ""
        inp.disabled = False
        inp.focus()
        for btn in self.query("Button"):
            btn.remove_class("-active")
        self.query_one(f"#opt-{idx}").add_class("-active")
        self.query_one("#message").update("")
        self.query_one("#progressbar").update("")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.in_progress or self.selected_index < 0:
            return
        val = event.value.strip()
        input_type = OPTIONS[self.selected_index][1]
        if not validate_input(input_type, val):
            self.query_one("#message").update(f"[red]Valor inválido para {OPTIONS[self.selected_index][0]}[/red]")
            return

        self.in_progress = True
        await self.run_worker(val)

    @work
    async def run_worker(self, val):
        pb = self.query_one("#progressbar")
        for i in range(101):
            pb.set_progress(i)
            await asyncio.sleep(0.03)
        self.in_progress = False
        self.finish_message(val)

    def finish_message(self, val):
        msg = (
            f"[green]Concluído![/green]\n\n"
            f"[yellow]{QUANTITY} itens processados[/yellow] para: [b white]{val}[/b white]\n\n"
            "[b cyan]DCL Tools - Apenas demonstrativo[/b cyan]"
        )
        self.query_one("#message").update(msg)
        inp = self.query_one("#input")
        inp.disabled = False
        inp.value = ""
        inp.focus()

if __name__ == "__main__":
    DCLApp().run()
