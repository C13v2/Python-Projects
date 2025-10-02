
import os
import logging
import json

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

Telegram_Bot_Token = os.getenv("Telegram_Bot_Token")
OpenAI_API_Key = os.getenv("OpenAI_API_Key")
SerpAPI_Key = os.getenv("SerpAPI_Key")

client = OpenAI(api_key=OpenAI_API_Key)
Chat_History = "chat_history.json"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def load_history():
    if os.path.exists(Chat_History):
        with open(Chat_History, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(Chat_History, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def google_search(query: str):
    search = GoogleSearch({
        "q": query,
        "hl": "it",
        "gl": "it",
        "api_key": SerpAPI_Key
    })
    results = search.get_dict()
    if "organic_results" in results:
        return results["organic_results"][:5]
    return []


# Bot logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I'm your Assistant! Tell me what you need.")

async def storico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat_id)
    history = load_history()
    if user_id not in history or not history[user_id]:
        await update.message.reply_text("No History")
        return
    testo = "\n\n".join([f"{m['role']}: {m['content']}" for m in history[user_id][-20:]])
    await update.message.reply_text("History:\n\n" + testo[:4000])

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat_id)
    user_input = update.message.text

    logging.info(f"User {user_id} asked: {user_input}")

    history = load_history()
    history.setdefault(user_id, [])

    # GPT decide se serve Google
    try:
        decision = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Decidi se la seguente domanda richiede una ricerca aggiornata su Google. Rispondi solo con 'YES' o 'NO'."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=3
        )
        decision_text = decision.choices[0].message.content.strip().upper()
        print(f"Decision: {decision_text}")
        logging.info(f"Decision for '{user_input}': {decision_text}")
    except Exception as e:
        decision_text = "NO"
        logging.error(f"Error deciding search: {e}")

    # Se serve, fai ricerca Google
    if decision_text == "YES":
        results = google_search(user_input)
        if results:
            links_text = "\n".join([f"{r.get('title', 'No title')} → {r.get('link', 'No link')}" for r in results])

            # Riassumo con GPT i risultati
            summary = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sei un assistente che riassume risultati di ricerca per l'utente in modo chiaro e utile."},
                    {"role": "user", "content": f"Domanda: {user_input}\n\nResult:\n{links_text}"}
                ]
            )
            reply = summary.choices[0].message.content + "\n\n Link:\n" + links_text
        else:
            reply = "No Result Found."
    else:

        # Risposta GPT diretta
        conversation = [{"role": "system", "content": "Sei un assistente utile con memoria."}]
        for msg in history[user_id][-10:]:
            conversation.append(msg)
        conversation.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = " AI Error: " + str(e)
            logging.error(f"Error GPT response: {e}")

    # Salva nello storico
    history[user_id].append({"role": "user", "content": user_input})
    history[user_id].append({"role": "assistant", "content": reply})
    save_history(history)

    logging.info(f"Reply to {user_id}: {reply[:100]}...")  # salvo solo i primi 100 caratteri nel log
    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(Telegram_Bot_Token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("storico", storico))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT Started")
    logging.info("BOT Started")
    app.run_polling()

if __name__ == "__main__":
    main()
