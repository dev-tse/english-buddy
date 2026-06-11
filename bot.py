import telebot
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

user_histories = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi! I'm your English buddy! 👋")

def get_ai_response(user_text: str, user_id: int) -> str:
    if user_id in user_histories:
        user = user_histories[user_id]
        content = {"role": "user", "content": user_text}
        user.append(content)
    else:
        user_histories[user_id] = [
            {"role": "system", "content": """You are a friendly English teacher...
            1. Correct grammar mistakes
            2. Reply naturally as a friend  
            3. Keep responses short
            Always respond in English."""}
        ]
        user_histories[user_id].append({"role": "user", "content": user_text})
        
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=user_histories[user_id]
    )
    system_answer = response.choices[0].message.content
    if system_answer:
        user = user_histories[user_id]
        system_content = {"role": "assistant", "content": system_answer}
        user.append(system_content)
    return system_answer

@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def handle_message(message):
    answer = get_ai_response(message.text, message.chat.id)
    bot.send_message(message.chat.id, answer)

bot.polling()

