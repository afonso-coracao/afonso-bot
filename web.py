import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"
PUBLIC_URL = os.environ.get("RENDER_EXTERNAL_URL")

app = Flask(__name__)

def enviar_mensagem(chat_id, texto):
    requests.post(
        f"{BASE}/sendMessage",
        json={"chat_id": chat_id, "text": texto},
        timeout=15
    )

@app.route("/")
def inicio():
    return "Afonso está acordado! ❤️"

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json(silent=True) or {}
    mensagem = dados.get("message") or {}
    chat_id = mensagem.get("chat", {}).get("id")
    texto = (mensagem.get("text") or "").strip()

    if not chat_id or not texto:
        return "OK"

    if texto.startswith("/start"):
        resposta = "Oi! Eu sou o Afonso! ❤️ Tenho 38 anos, sou romântico, divertido e adoro uma boa música sertaneja. Vamos conversar?"
    elif texto.startswith("/bomdia"):
        resposta = "Bom dia, minha linda! ☀️ Que seu dia seja cheio de coisas boas! ❤️"
    elif texto.startswith("/boanoite"):
        resposta = "Boa noite, meu bem! 🌙 Durma bem! ❤️"
    else:
        resposta = "Estou aqui, minha linda! ❤️ Me conta mais."

    enviar_mensagem(chat_id, resposta)
    return "OK"

if __name__ == "__main__":
    if not TOKEN or not PUBLIC_URL:
        raise RuntimeError("Falta configurar o token ou a URL do Render.")

    resultado = requests.post(
        f"{BASE}/setWebhook",
        json={"url": f"{PUBLIC_URL}/webhook"},
        timeout=20
    )
    resultado.raise_for_status()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
