import os
import re
import time
from datetime import datetime

# -------------------------------
# Configurações e opções do painel
# -------------------------------
OPTIONS = [
    ("SMS Básico", "phone", "Envia SMS para números válidos."),
    ("Ligações", "phone", "Faz ligações automáticas."),
    ("E-mail", "email", "Envia e-mails válidos."),
    ("WhatsApp", "phone", "Envia mensagens pelo WhatsApp."),
    ("Redes Sociais", "username", "Envia mensagens para perfis sociais."),
    ("Telegram", "username", "Envia mensagens para contatos do Telegram."),
    ("Direcionado", "username", "Envio direcionado a um alvo específico."),
    ("Em Massa", "username", "Envio em grande quantidade."),
    ("Com Links", "link", "Envia mensagens contendo links."),
    ("Programado", "programado", "Programar envio Hoje ou Amanhã."),
]

QUANTITY = 50  # quantidade simulada de envio

# -------------------------------
# Funções auxiliares
# -------------------------------
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    now = datetime.now()
    print("╔══════════════════════════════════╗")
    print("║          DCL SPAM TOOL           ║")
    print(f"║  {now.strftime('%d/%m/%Y')}    {now.strftime('%H:%M:%S')}       ║")
    print("╚══════════════════════════════════╝\n")

def print_menu():
    print("📋 MENU DE OPÇÕES:\n")
    for i, (label, _, _) in enumerate(OPTIONS, 1):
        print(f"{i:2d}. {label}")
    print("\n0. Sair\n")

def validate_input(input_type, value):
    patterns = {
        "phone": r"^[+]?[\d\s()-]{8,15}$",
        "email": r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        "username": r"^[a-zA-Z0-9._]{3,25}$",
        "link": r"^https?://.+$",
        "programado": r"[HhAa]"
    }
    pattern = patterns.get(input_type)
    if pattern:
        return re.match(pattern, value.strip()) is not None
    return False

def input_value(prompt, input_type):
    while True:
        val = input(prompt).strip()
        if input_type == "programado":
            if val.lower() in ["h", "a"]:
                return "Hoje" if val.lower()=="h" else "Amanhã"
            else:
                print("⚠️ Digite H para Hoje ou A para Amanhã.")
        elif validate_input(input_type, val):
            return val
        else:
            print("⚠️ Entrada inválida! Tente novamente.")

def simulate_progress(task_name):
    size = 30
    for i in range(1, QUANTITY+1):
        percent = int(i * 100 / QUANTITY)
        filled = int(size * percent / 100)
        bar = "[" + "█"*filled + " "*(size-filled) + "]"
        print(f"\r{task_name}: {bar} {percent}% ({i}/{QUANTITY})", end="")
        time.sleep(0.05)
    print("\n✅ Concluído!\n")

def print_footer():
    print("✦ Doctor Coringa Lunático ✦")
    print('"Transformando códigos em caos organizado"')
    print("\n" + "="*40 + "\n")

# -------------------------------
# Loop principal
# -------------------------------
def main():
    while True:
        clear()
        print_banner()
        print_menu()
        choice = input("Digite o número da opção e pressione ENTER: ").strip()
        if choice == "0":
            print("\nSaindo do painel... Até logo! 👋")
            break
        if not choice.isdigit() or int(choice)<1 or int(choice)>len(OPTIONS):
            print("⚠️ Opção inválida! Pressione ENTER para tentar novamente.")
            input()
            continue
        idx = int(choice) - 1
        option_label, option_type, description = OPTIONS[idx]
        clear()
        print_banner()
        print(f"🔹 Você escolheu: {option_label}")
        print(f"💬 {description}\n")
        if option_type == "programado":
            val = input_value("Escolha Hoje (H) ou Amanhã (A): ", option_type)
        else:
            val = input_value("Digite o valor: ", option_type)
        simulate_progress(option_label)
        print(f"🎯 {QUANTITY} itens processados para '{val}'\n")
        print_footer()
        input("Pressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    main()
