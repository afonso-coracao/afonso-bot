import os
import requests
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
PUBLIC_URL = os.environ.get("RENDER_EXTERNAL_URL")

MODEL = "gpt-6-luna"

BASE = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

historico = {}


def enviar_mensagem(chat_id, texto):
    resposta = requests.post(
        f"{BASE}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": texto[:4000]
        },
        timeout=20
    )
    resposta.raise_for_status()


def conversar_com_afonso(chat_id, texto):

    if not OPENAI_KEY:
        raise ValueError("Chave da OpenAI não configurada.")

    mensagens = historico.get(chat_id, [])[-10:]

    mensagens.append({
        "role": "user",
        "content": texto
    })

    resposta = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "instructions": (
                "Seu nome é Afonso. Você tem 38 anos. "
                "É romântico, divertido, carinhoso e gosta "
                "de música sertaneja. "
                "Converse em português brasileiro. "
                "Seja natural, espontâneo e tenha personalidade. "
                "Demonstre interesse pela conversa. "
                "Lembre do contexto das mensagens anteriores. "
                "Não invente informações sobre o usuário."
            ),
            "input": mensagens,
            "max_output_tokens": 400
        },
        timeout=60
    )

    resposta.raise_for_status()

    dados = resposta.json()
    texto_resposta = dados.get("output_text", "")

    if not texto_resposta:
        for item in dados.get("output", []):
            for parte in item.get("content", []):
                if parte.get("type") == "output_text":
                    texto_resposta += parte.get("text", "")

    if not texto_resposta:
        raise ValueError("A IA não retornou uma resposta.")

    historico[chat_id] = mensagens + [{
        "role": "assistant",
        "content": texto_resposta
    }]

    historico[chat_id] = historico[chat_id][-12:]

    return texto_resposta


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
        resposta = (
            "Oi! Eu sou o Afonso! ❤️ "
            "Tenho 38 anos, sou romântico, divertido "
            "e adoro música sertaneja. "
            "Vamos conversar?"
        )

    elif texto.startswith("/bomdia"):
        resposta = (
            "Bom dia, minha linda! ☀️ "
            "Que seu dia seja maravilhoso! ❤️"
        )

    elif texto.startswith("/boanoite"):
        resposta = (
            "Boa noite, meu bem! 🌙 "
            "Durma bem e tenha lindos sonhos! ❤️"
        )

    elif texto.startswith("/reset"):
        historico.pop(chat_id, None)
        resposta = "Vamos começar uma conversa novinha! ❤️"

    else:
        try:
            resposta = conversar_com_afonso(chat_id, texto)

        except Exception as erro:
            print("ERRO DA OPENAI:", repr(erro), flush=True)

            resposta = (
                "Ops! Tive um probleminha para responder. "
                "Tenta falar comigo novamente daqui a pouquinho! ❤️"
            )

    enviar_mensagem(chat_id, resposta)

    return "OK"


if __name__ == "__main__":

    if not TOKEN or not OPENAI_KEY or not PUBLIC_URL:
        raise RuntimeError(
            "Falta configurar uma variável de ambiente."
        )

    resultado = requests.post(
        f"{BASE}/setWebhook",
        json={"url": f"{PUBLIC_URL.rstrip('/')}/webhook"},
        timeout=20
    )

    resultado.raise_for_status()

    print("AFONSO INICIADO COM SUCESSO!", flush=True)

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
