import curses
import time
import os
import re
from datetime import datetime, timedelta

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

ALERTA_SOM = "/sdcard/alert.mp3"  # Caminho do som de alerta

def gerar_menu(max_x):
    largura = min(max_x - 2, 50)
    if largura < 30:
        largura = 30
    topo = "╔" + "═" * (largura - 2) + "╗"
    meio = "╠" + "═" * (largura - 2) + "╣"
    fundo = "╚" + "═" * (largura - 2) + "╝"

    linhas = [
        topo,
        "║   📌 SPAM 📌   ".ljust(largura - 1) + "║",
        "║ 🇱🇻 Doctor Coringa".ljust(largura - 1) + "║",
        meio,
        "║     PAINEL     ║",
        meio
    ]
    for idx, (nome, _, _) in enumerate(SPAM_OPTIONS, 1):
        linhas.append(f"║ {idx:2d}. {nome}".ljust(largura - 1) + "║")
    linhas.append(fundo)
    return linhas

def limpar_tela():
    os.system('clear' if os.name == 'posix' else 'cls')

def validar_numero(valor):
    return valor.isdigit() and len(valor) >= 8

def validar_email(valor):
    return re.match(r"[^@]+@[^@]+\.[^@]+", valor) is not None

def validar_link(valor):
    return valor.startswith("http://") or valor.startswith("https://")

def pedir_entrada(stdscr, prompt, max_len=30, y_pos=0):
    curses.echo()
    stdscr.addstr(y_pos, 0, " " * 60)
    stdscr.addstr(y_pos, 0, prompt)
    stdscr.move(y_pos, len(prompt))
    entrada = stdscr.getstr(y_pos, len(prompt), max_len).decode().strip()
    curses.noecho()
    return entrada

def tocar_alerta():
    if os.path.exists(ALERTA_SOM):
        os.system(f"termux-media-player play '{ALERTA_SOM}'")
    else:
        curses.beep()

def aguardar_programado(stdscr):
    while True:
        escolha = pedir_entrada(stdscr, "Escolha Hoje (H) ou Amanhã (A): ", y_pos=16).lower()
        if escolha in ["h", "a"]:
            return escolha
        else:
            stdscr.addstr(17, 0, "Opção inválida! Digite H ou A.", curses.color_pair(2))
            stdscr.refresh()
            time.sleep(1.5)

def enviar_spam(alvo, tipo_spam, qtd, stdscr):
    limpar_tela()
    stdscr.clear()
    msg_aguarde_base = "Aguarde... Enviando spam "
    anim_frames = ["|", "/", "-", "\\"]
    max_y, max_x = stdscr.getmaxyx()
    largura_barra = max_x - 20
    if largura_barra < 10:
        largura_barra = 10

    try:
        stdscr.addstr(0, 0, f"Enviando '{tipo_spam}' para '{alvo}' ({qtd} spam(s))..."[:max_x-1], curses.color_pair(2))
    except curses.error:
        pass
    stdscr.refresh()

    for i in range(1, qtd + 1):
        progresso = i / qtd
        chars_barras = int(progresso * largura_barra)
        barra = "[" + "#" * chars_barras + "-" * (largura_barra - chars_barras) + "]"
        perc = int(progresso * 100)
        spinner = anim_frames[i % len(anim_frames)]
        linha_progresso = f"{i:03d}/{qtd:03d} {barra} {perc:3d}%"
        linha_aguarde = f"{msg_aguarde_base}{spinner}"
        try:
            stdscr.addstr(2, 0, linha_progresso[:max_x-1], curses.color_pair(1))
            stdscr.clrtoeol()
            stdscr.addstr(4, 0, linha_aguarde[:max_x-1], curses.color_pair(3))
            stdscr.clrtoeol()
            stdscr.refresh()
        except curses.error:
            pass
        time.sleep(0.15)

    try:
        stdscr.addstr(6, 0, "✅ Envio concluído! Pressione qualquer tecla para voltar."[:max_x-1], curses.color_pair(4))
        stdscr.clrtoeol()
        stdscr.refresh()
    except curses.error:
        pass
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        MENU_TEXT = gerar_menu(max_x)
        for i, line in enumerate(MENU_TEXT):
            if i >= max_y - 6:  
                break
            stdscr.addstr(i, 0, line[:max_x-1])

        y_input = len(MENU_TEXT) + 1
        stdscr.addstr(y_input, 0, "Digite a opção (1-10) ou Q para sair: ", curses.color_pair(4))
        stdscr.refresh()
        tecla = pedir_entrada(stdscr, "", y_pos=y_input)

        if tecla.lower() == 'q':
            break

        if tecla.isdigit():
            opcao = int(tecla)
            if 1 <= opcao <= 10:
                tipo_spam, tipo_entrada, descricao = SPAM_OPTIONS[opcao -1]

                stdscr.clear()
                stdscr.addstr(0, 0, f"Você escolheu: {tipo_spam}")
                stdscr.addstr(1, 0, descricao)
                stdscr.refresh()
                time.sleep(2)  # pequena pausa para leitura

                alvo = ""
                while tipo_entrada != "programado":
                    stdscr.clear()
                    stdscr.addstr(0, 0, f"Alvo para '{tipo_spam}': ")
                    alvo = pedir_entrada(stdscr, "", y_pos=1)
                    valido = False
                    if tipo_entrada == "numero":
                        valido = validar_numero(alvo)
                    elif tipo_entrada == "email":
                        valido = validar_email(alvo)
                    elif tipo_entrada == "link":
                        valido = validar_link(alvo)
                    else:
                        valido = len(alvo) > 0

                    if not valido:
                        stdscr.addstr(2, 0, "Entrada inválida! Tente novamente.", curses.color_pair(2))
                        stdscr.refresh()
                        time.sleep(1.5)
                    else:
                        break

                if tipo_entrada == "programado":
                    escolha_dia = aguardar_programado(stdscr)
                    alvo = f"Programado para {'Hoje' if escolha_dia=='h' else 'Amanhã'}"

                enviar_spam(alvo, tipo_spam, 60, stdscr)
        else:
            stdscr.addstr(max_y-2, 0, "Opção inválida! Digite 1 a 10 ou Q para sair.", curses.color_pair(2))
            stdscr.refresh()
            time.sleep(1.5)

if __name__ == "__main__":
    curses.wrapper(main)
