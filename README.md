🚀 Spam Panel - Termux

Painel interativo de envio de mensagens via SMS, WhatsApp, Telegram e e-mails, diretamente no Termux.

> ⚠️ Aviso Importante: Este painel não deve ser usado com números próprios ou de terceiros sem autorização. Seu uso é estritamente educacional e de teste.

🎉 Tela de Boas-Vindas

Ao iniciar o painel, você verá algo assim no Termux:

##############################################
#                                            #
#          WELCOME TO SPAM PANEL             #
#                                            #
#  Interactive Panel - SMS / WhatsApp /     #
#       Telegram / Email Automation          #
#                                            #
##############################################

Select an option by entering its number:

> 💡 A interface é clara, interativa e totalmente navegável via teclado, digitando apenas números.

---

✨ Funcionalidades

🎨 Interface interativa no terminal via Textual

📱 Envio de mensagens via SMS, WhatsApp, Telegram

📧 Envio de e-mails em massa

🔢 Navegação fácil usando apenas números

⚡ Configuração rápida e aprendizado prático



---

🛠️ Requisitos

Termux atualizado

Python 3 (já incluso no Termux)

Git



---

🔍 Passo a Passo

1️⃣ Atualizar pacotes do Termux

pkg update -y && pkg upgrade -y

Atualiza todos os pacotes e evita problemas de compatibilidade.



---

2️⃣ Instalar Python e Git

pkg install python git -y

python → necessário para executar o painel.

git → usado para clonar o repositório.



---

3️⃣ Instalar dependências Python

python3 -m pip install --upgrade requests textual

requests → permite envio de requisições HTTP.

textual → cria interface interativa no terminal.


> ⚠️ No Termux moderno, não é necessário instalar pip separadamente.

---

4️⃣ Clonar o repositório

git clone https://github.com/DOCTORcoringa/.Spam.py

Baixa todos os arquivos do painel para o Termux.


---

5️⃣ Entrar na pasta do projeto

cd .Spam.py

Navega até o diretório onde o script está localizado.



---

6️⃣ Executar o painel

python3 spam.py

Abre a interface interativa.

Escolha as opções digitando apenas os números correspondentes

---

🔥 Sugestões de Uso

Nunca use números próprios ou de terceiros sem autorização.

Teste apenas em ambientes controlados ou números de teste.

Use o Termux em modo paisagem ou tela cheia para melhor visualização.

Explore todas as funcionalidades para aprendizado de automação e testes.



---

📄 Licença

Este projeto está licenciado sob a MIT License.
