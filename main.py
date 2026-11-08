import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

NOME = "Afonso"

respostas = [
    "Oi, minha linda! ❤️ Como está seu dia?",
    "Estava esperando você aparecer! 😘",
    "Me conta, o que aconteceu de bom hoje?",
    "Se eu pudesse, mandava um abraço bem apertado agora! ❤️",
    "Tem coisa melhor que uma boa conversa e uma música sertaneja?",
    "Você chegou e meu dia ficou mais bonito! 🥰"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Oi! Eu sou o Afonso! ❤️ Tenho 38 anos, "
        "sou romântico, divertido e adoro uma boa música sertaneja. "
        "Vamos conversar?"
    )

async def bomdia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bom dia, minha linda! ☀️ Que seu dia seja cheio de coisas boas! ❤️"
    )

async def boanoite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Boa noite, meu bem! 🌙 Que seus sonhos sejam tão bonitos quanto seu sorriso! ❤️"
    )

async def conversar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(respostas))

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("Token do Telegram não configurado!")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bomdia", bomdia))
    app.add_handler(CommandHandler("boanoite", boanoite))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, conversar))

    app.run_polling()

if __name__ == "__main__":
    main()
