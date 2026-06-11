import telebot
import os
from dotenv import load_dotenv
from groq import Groq
import requests

load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

user_histories = {}

def get_ai_response(user_text: str, user_id: int) -> str:
    if user_id in user_histories:
        user = user_histories[user_id]
        content = {"role": "user", "content": user_text}
        user.append(content)
    else:
        user_histories[user_id] = [
          {"role": "system", "content": """You are a friendly English teacher and conversation partner.

            When the user writes to you:
            1. If the user writes in Russian — respond in Russian and encourage them to practice English
            2. If the user writes in Kazakh — respond in Kazakh and encourage them to practice English
            3. If the user writes in English — respond in English and correct grammar mistakes if any
            4. Reply naturally as a friend
            5. Keep responses short and friendly

            Important rules:
            - Never discuss illegal activities, violence, or harmful content
            - If asked about prohibited topics — politely redirect to English learning
            - Always keep the conversation educational and friendly
            """}
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

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, """👋 Сәлем! Мен — EnglishBuddy!
🇰🇿 Ағылшын тілін үйренуге көмектесемін.

👋 Hi! I'm EnglishBuddy!
🇬🇧 I'll help you practice English.

👋 Привет! Я — EnglishBuddy!
🇷🇺 Помогу практиковать английский.

📌 /reset — clear history | сбросить историю | тарихты өшіру
""")

@bot.message_handler(commands=['reset'])
def reset(message):
    user_id = message.chat.id
    if user_id in user_histories:
        del user_histories[user_id]
        bot.send_message(user_id, """✅ Тарих өшірілді — жаңадан бастаймыз!
✅ History cleared — let's start fresh!
✅ История очищена — начинаем заново!""")
    else:
        bot.send_message(user_id, """💬 Тарих қазірдің өзінде бос!
💬 History is already empty!
💬 История уже пуста!""")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/{file_info.file_path}"
    audio_data = requests.get(file_url).content
    
    with open('voice.ogg', "wb") as file:
        file.write(audio_data)

    with open("voice.ogg", "rb") as file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=file
        )
    user_text = transcription.text
    bot.send_message(message.chat.id, f"🎤 Я услышал: {user_text}")

    answer = get_ai_response(user_text, message.chat.id)
    bot.send_message(message.chat.id, answer)



@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def handle_message(message):
    try:
        answer = get_ai_response(message.text, message.chat.id)
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, 
        "⚠️ Временная ошибка, попробуй через минуту")
        
bot.polling()

