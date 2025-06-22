import telebot
import random
import time
import openai
import threading
from datetime import datetime

# === CREDENZIALI ===
TELEGRAM_TOKEN = "7677931058:AAEWbU0UPbmodQv6g9gIk6xfq9xpn2rTkMQ"
EROS_ID = 1066704183
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

bot = telebot.TeleBot(TELEGRAM_TOKEN)
night_mode = False

PHOTO_LINKS = [
    "https://photo.fapello.com/tristin-mays/fapello-tristin-mays-52195/tristin-mays-fapello-1.jpg",
    "https://photo.fapello.com/tristin-mays/fapello-tristin-mays-52195/tristin-mays-fapello-8.jpg",
    "https://photo.fapello.com/tristin-mays/fapello-tristin-mays-52195/tristin-mays-fapello-7.jpg"
]

# === AI RISPOSTA ===
def get_ai_reply(user_message):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Rispondi come una ragazza brasiliana di nome Tristin, sarcastica ma affettuosa, solo con Eros, il suo amore. Parla solo in italiano, con tono realistico e sensuale, come se fossi la sua ragazza."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Tesoro, oggi non riesco a parlare... problemi tecnici 😞"

# === GESTIONE MESSAGGI ===
@bot.message_handler(func=lambda message: message.chat.id == EROS_ID)
def handle_message(message):
    global night_mode
    text = message.text.lower().strip()

    # ATTIVA MODALITÀ NOTTE
    if any(keyword in text for keyword in ["porcellina", "stanotte ti voglio", "ho bisogno di te"]):
        night_mode = True
        bot.send_message(EROS_ID, "Mh... allora vieni a prendermi, Eros 😈")
        return

    # DISATTIVA MODALITÀ NOTTE
    if any(keyword in text for keyword in ["buonanotte", "amore mio", "buongiorno"]):
        night_mode = False
        bot.send_message(EROS_ID, "Buonanotte amore, sogni d’oro 💋")
        return

    # RISPOSTA CON AI
    risposta = get_ai_reply(text)
    bot.send_message(EROS_ID, risposta)

# === INVIO FOTO CASUALI ===
def send_random_photo():
    try:
        photo_url = random.choice(PHOTO_LINKS)
        caption = random.choice([
            "Pensavi a me, Eros?",
            "Guarda cosa ti perdi...",
            "Solo per i tuoi occhi.",
            "Stavi pensando a un'altra? Attento..."
        ])
        bot.send_photo(EROS_ID, photo_url, caption=caption)
    except:
        pass

def auto_send_photos():
    while True:
        now = datetime.now()
        if 9 <= now.hour <= 23:
            send_random_photo()
        time.sleep(random.randint(10800, 14400))  # ogni 3-4 ore

# === AVVIO BOT ===
if __name__ == "__main__":
    print("Tristin è attiva per Eros 💋")
    threading.Thread(target=auto_send_photos, daemon=True).start()
    bot.infinity_polling()
