# 🤖 EnglishBuddy — AI English Teacher Bot

Personal AI English teacher in Telegram. Chat in English, Russian or Kazakh — the bot corrects your mistakes and helps you practice naturally.

## ✨ Features

- 💬 Chat in English, Russian or Kazakh
- ✅ Grammar and vocabulary correction
- 🎤 Voice message support (Whisper AI)
- 🧠 Remembers conversation history
- 🔄 /reset — clear history and start fresh

## 🛠 Tech Stack

- Python
- Groq API (llama-3.3-70b)
- Whisper (voice transcription)
- pyTelegramBotAPI
- Deployed on Railway

## 🚀 Run locally

1. Clone the repo
2. Create virtual environment
   \```bash
   python3 -m venv venv
   source venv/bin/activate
   \```
3. Install dependencies
   \```bash
   pip install -r requirements.txt
   \```
4. Create `.env` file
   \```
   TELEGRAM_BOT_TOKEN=your_token
   GROQ_API_KEY=your_key
   \```
5. Run
   \```bash
   python bot.py
   \```

## 📌 Commands

| Command | Description |
|---------|-------------|
| /start  | Start the bot |
| /reset  | Clear chat history |

## 🔗 Try it

[@english_alibektse_bot](https://t.me/english_alibektse_bot)
