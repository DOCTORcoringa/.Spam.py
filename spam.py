import curses
import time
import os
import re
from datetime import datetime, timedelta

SPAM_OPTIONS = [
    ("SMS Básico", "numero"),
    ("Ligações", "numero"),
    ("E-mail", "email"),
    ("WhatsApp", "numero"),
    ("Redes Sociais", "texto"),
    ("Telegram", "texto"),
    ("Direcionado", "texto"),
    ("Em Massa", "texto"),
    ("Com Links", "link"),
    ("Programado", "texto")
]

# Caminho do som de alerta no seu celular
ALERTA_SOM = "/sdcard/alert.mp3"  # substitua pelo caminho do seu arquivo

def gerar_menu(max_x):
    largura = min(max_x - 2, 32)
    if largura < 20:
        largura = 20

    topo = "╔" + "═" * (largura - 2) + "╗"
    meio = "╠" + "═" * (largura - 2) + "╣"
    fundo = "╚" + "═" * (largura - 2) + "╝"

    linhas = [
        topo,
        "║   📌 SPAM 📌   ".ljust(largura - 1) + "║",
        "║ 🇱🇻 Doctor Coringa".ljust(largura - 1) + "║",
        meio,
        "║     PAINEL".ljust(largura - 1) + "║",
        meio,
        "║ 🇱🇻 1. SMS Básico".ljust(largura - 1) + "║",
        "║ 🇱🇻 2. Ligações".ljust(largura - 1) + "║",
        "║ 🇱🇻 3. E-mail".ljust(largura - 1) + "║",
        "║ 🇱🇻 4. WhatsApp".ljust(largura - 1) + "║",
        "║ 🇱🇻 5. Redes Sociais".ljust(largura - 1) + "║",
        "║ 🇱🇻 6. Telegram".ljust(largura - 1) + "║",
        "║ 🇱🇻 7. Direcionado".ljust(largura - 1) + "║",
        "║ 🇱🇻 8. Em Massa".ljust(largura - 1) + "║",
        "║ 🇱🇻 9. Com Links".ljust(largura - 1) + "║",
        "║ 🇱🇻10. Programado".ljust(largura - 1) + "║",
        fundo
    ]
    return linhas

def limpar_tela():
    os.system('clear' if os.name == 'posix' else 'cls')

def validar_numero(valor):
    return valor.isdigit() and len(valor) >= 8

def validar_email(valor):
    return re.match(r"[^@]+@[^@]+\.[^@]+", valor) is not None

def validar_link(valor):
    return valor.startswith("http://") or valor.startswith("https://")

def validar_hora(hora_str):
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True
    except:
        return False

def pedir_entrada(stdscr, prompt, max_len=30):
    curses.echo()
    stdscr.addstr(16, 0, " " * 60)
    stdscr.addstr(16, 0, prompt)
    stdscr.move(16, len(prompt))
    entrada = stdscr.getstr(16, len(prompt), max_len).decode().strip()
    curses.noecho()
    return entrada

def tocar_alerta():
    if os.path.exists(ALERTA_SOM):
        os.system(f"termux-media-player play '{ALERTA_SOM}'")
    else:
        curses.beep()  # fallback se arquivo não existir

def aguardar_hora(stdscr, hora_programada):
    spinner_frames = ["|", "/", "-", "\\"]
    idx = 0
    tocou_alerta = False
    while True:
        agora = datetime.now()
        if agora >= hora_programada and not tocou_alerta:
            tocar_alerta()
            tocou_alerta = True
            break  # sai do loop ou deixa continuar se quiser ver o tempo 0
        falta = (hora_programada - agora).total_seconds()
        if falta < 0:
            falta = 0
        horas = int(falta // 3600)
        minutos = int((falta % 3600) // 60)
        segundos = int(falta % 60)
        msg = f"⏳ Enviando em {horas:02d}:{minutos:02d}:{segundos:02d}  "
        max_y, max_x = stdscr.getmaxyx()
        try:
            stdscr.addstr(max_y-4, 0, msg[:max_x-2], curses.color_pair(2))
            stdscr.clrtoeol()
            # spinner no canto direito
            stdscr.addstr(max_y-4, max_x-2, spinner_frames[idx % len(spinner_frames)], curses.color_pair(3))
            stdscr.refresh()
        except curses.error:
            pass
        time.sleep(0.2)
        idx += 1

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
        try:
            for i, line in enumerate(MENU_TEXT):
                if i >= max_y - 6:  
                    break
                stdscr.addstr(i, 0, line[:max_x-1])
            msg_instrucoes = "Digite o número da opção (1-10), ou Q para sair:"
            linha_instr = min(len(MENU_TEXT), max_y-2)
            stdscr.addstr(linha_instr, 0, msg_instrucoes[:max_x-1], curses.color_pair(4))
            stdscr.refresh()
            tecla = stdscr.getkey()
        except curses.error:
            tecla = ''

        if tecla.lower() == 'q':
            break

        if tecla.isdigit():
            opcao = int(tecla)
            if 1 <= opcao <= 10:
                tipo_spam, tipo_entrada = SPAM_OPTIONS[opcao -1]

                alvo = ""
                while True:
                    stdscr.clear()
                    try:
                        stdscr.addstr(0, 0, f"Alvo para '{tipo_spam}': "[:max_x-1])
                    except curses.error:
                        pass
                    alvo = pedir_entrada(stdscr, "", max_len=max_x-1)
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
                        try:
                            stdscr.addstr(2, 0, "Entrada inválida! Tente novamente."[:max_x-1], curses.color_pair(2))
                            stdscr.refresh()
                        except curses.error:
                            pass
                        time.sleep(1.5)
                    else:
                        break

                hora_valida = False
                while not hora_valida:
                    stdscr.clear()
                    try:
                        stdscr.addstr(0, 0, "Horário envio (HH:MM 24h): "[:max_x-1])
                    except curses.error:
                        pass
                    hora_str = pedir_entrada(stdscr, "", max_len=max_x-1)
                    if validar_hora(hora_str):
                        hora_valida = True
                    else:
                        try:
                            stdscr.addstr(2, 0, "Horario inválido! Use HH:MM formato 24h"[:max_x-1], curses.color_pair(2))
                            stdscr.refresh()
                        except curses.error:
                            pass
                        time.sleep(1.5)

                agora = datetime.now()
                hora_entrega = datetime.strptime(hora_str, "%H:%M").replace(
                    year=agora.year, month=agora.month, day=agora.day
                )
                if hora_entrega < agora:
                    hora_entrega += timedelta(days=1)

                stdscr.clear()
                try:
                    texto_agendado = f"📅 Agendado '{tipo_spam}' para '{alvo}' às {hora_str}."
                    stdscr.addstr(0, 0, texto_agendado[:max_x-1])
                    stdscr.refresh()
                except curses.error:
                    pass

                aguardar_hora(stdscr, hora_entrega)
                enviar_spam(alvo, tipo_spam, 60, stdscr)
        else:
            try:
                stdscr.addstr(max_y-2, 0, "Opção inválida! Digite 1 a 10 ou Q para sair."[:max_x-1], curses.color_pair(2))
                stdscr.refresh()
            except curses.error:
                pass
            time.sleep(1.5)

if __name__ == "__main__":
    curses.wrapper(main)
