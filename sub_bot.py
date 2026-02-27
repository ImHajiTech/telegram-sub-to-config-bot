import base64
import requests
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


def is_base64(s: str) -> bool:
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n\n"
        "برای تبدیل لینک سابسکریپشن به کانفیگ،\n"
        "لطفاً لینک ساب خودتون رو ارسال کنید 🔗"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.startswith("http"):
        await update.message.reply_text(
            "❌ لطفاً یک لینک سابسکریپشن معتبر ارسال کنید"
        )
        return

    try:
        response = requests.get(text, timeout=15)
        content = response.text.strip()

        if content.startswith("{") or content.startswith("["):
            decoded = content
        else:
            if is_base64(content):
                decoded = base64.b64decode(content).decode(
                    "utf-8", errors="ignore"
                )
            else:
                decoded = content

        if not decoded.strip():
            await update.message.reply_text("❌ محتوای لینک خالی است")
            return

        if len(decoded) > 4000:
            parts = [decoded[i:i + 4000] for i in range(0, len(decoded), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(decoded)

    except Exception as e:
        await update.message.reply_text(f"❌ خطا در پردازش لینک:\n{e}")


def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN not set!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
