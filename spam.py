import curses
import re
import time

SPAM_OPTIONS = [
    ("SMS Básico", "numero", "Envia SMS para o número escolhido."),
    ("Ligações", "numero", "Faz ligações automáticas para o número."),
    ("E-mail", "email", "Envia e-mails para o endereço informado."),
    ("WhatsApp", "numero", "Envia mensagens pelo WhatsApp para o número."),
    ("Redes Sociais", "texto", "Envia mensagens para redes sociais selecionadas."),
    ("Telegram", "texto", "Envia mensagens para contatos do Telegram."),
    ("Direcionado", "texto", "Envia spam direcionado a um alvo específico."),
    ("Em Massa", "texto", "Envia spam em grande quantidade para múltiplos alvos."),
    ("Com Links", "link", "Envia mensagens contendo links."),
    ("Programado", "programado", "Permite programar o envio para Hoje ou Amanhã.")
]

def gerar_menu(max_y, max_x):
    largura = max_x - 4
    topo = "╔" + "═" * (largura-2) + "╗"
    fundo = "╚" + "═" * (largura-2) + "╝"
    meio = "╠" + "═" * (largura-2) + "╣"

    linhas = [
        topo,
        f"║{'📌 SPAM PAINEL AD4 📌'.center(largura-2)}║",
        f"║{'🇱🇻 Doctor Coringa'.center(largura-2)}║",
        meio,
        f"║{'MENU PRINCIPAL'.center(largura-2)}║",
        meio
    ]

    for idx, (nome, _, _) in enumerate(SPAM_OPTIONS, 1):
        linhas.append(f"║ {idx:2d}. {nome}".ljust(largura-1) + "║")

    linhas.append(fundo)
    return linhas

def pedir_entrada(stdscr, prompt, y_pos=0, x_pos=0, max_len=50):
    curses.echo()
    stdscr.addstr(y_pos, x_pos, " " * 100)
    stdscr.addstr(y_pos, x_pos, prompt)
    stdscr.move(y_pos, x_pos + len(prompt))
    entrada = stdscr.getstr(y_pos, x_pos + len(prompt), max_len).decode().strip()
    curses.noecho()
    return entrada

def validar_numero(valor):
    return valor.isdigit() and len(valor) >= 8

def validar_email(valor):
    return re.match(r"[^@]+@[^@]+\.[^@]+", valor) is not None

def validar_link(valor):
    return valor.startswith("http://") or valor.startswith("https://")

def obter_valor(stdscr, tipo_entrada):
    while True:
        entrada = pedir_entrada(stdscr, f"Digite o {tipo_entrada}: ", y_pos=10, x_pos=4)
        if tipo_entrada == "número" and validar_numero(entrada):
            return entrada
        elif tipo_entrada == "email" and validar_email(entrada):
            return entrada
        elif tipo_entrada == "link" and validar_link(entrada):
            return entrada
        elif tipo_entrada == "texto" and len(entrada) > 0:
            return entrada
        elif tipo_entrada == "programado":
            escolha = pedir_entrada(stdscr, "Programar para Hoje (H) ou Amanhã (A): ", y_pos=12, x_pos=4).lower()
            if escolha in ["h", "a"]:
                return "Hoje" if escolha == "h" else "Amanhã"
        stdscr.addstr(14, 4, "Entrada inválida. Tente novamente.")
        stdscr.refresh()
        time.sleep(1.5)
        stdscr.addstr(14, 4, " " * 50)

def enviar(stdscr, opcao_idx, valor):
    tipo_spam, _, descricao = SPAM_OPTIONS[opcao_idx]
    stdscr.clear()
    stdscr.addstr(2, 4, f"Opção escolhida: {tipo_spam}")
    stdscr.addstr(4, 4, descricao)
    stdscr.addstr(6, 4, f"Enviando para: {valor} ...")
    stdscr.refresh()

    for i in range(1, 61):
        barra = "#" * i
        stdscr.addstr(8, 4, f"[{barra:<60}] {i*100//60:3d}%")
        stdscr.refresh()
        time.sleep(0.03)

    stdscr.addstr(10, 4, "✅ Envio concluído! Pressione qualquer tecla para voltar ao menu.")
    stdscr.refresh()
    stdscr.getch()

def mostrar_menu(stdscr):
    curses.curs_set(1)
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        menu_text = gerar_menu(max_y, max_x)
        start_y = max(0, (max_y - len(menu_text)) // 2)

        for i, line in enumerate(menu_text):
            if start_y + i < max_y - 1:
                stdscr.addstr(start_y + i, 2, line[:max_x-4])

        input_y = start_y + len(menu_text) + 1
        escolha = pedir_entrada(stdscr, "Escolha a opção: ", y_pos=input_y, x_pos=4)

        if escolha.lower() == 'q':
            break

        if escolha.isdigit():
            opcao = int(escolha)
            if 1 <= opcao <= 10:
                tipo_spam, tipo_entrada, _ = SPAM_OPTIONS[opcao-1]
                if tipo_entrada == "numero":
                    valor = obter_valor(stdscr, "número")
                elif tipo_entrada == "email":
                    valor = obter_valor(stdscr, "email")
                elif tipo_entrada == "link":
                    valor = obter_valor(stdscr, "link")
                elif tipo_entrada == "programado":
                    valor = obter_valor(stdscr, "programado")
                else:
                    valor = obter_valor(stdscr, "texto")
                enviar(stdscr, opcao-1, valor)

if __name__ == "__main__":
    curses.wrapper(mostrar_menu)
