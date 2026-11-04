from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

# Подключаем оригинальный бесплатный API Kimi напрямую
client = OpenAI(
    base_url="https://moonshot.ai",
    api_key="sk-oDXjNRMxvFyE08iAxn0A03hfmw8KAL1GFxdkerIfDOyXFwTf"
)

"/marusia"
async def marusia_skill(request: Request):
    data = await request.json()
    user_phrase = data.get("request", {}).get("command", "")
    session = data.get("session", {})
    
    if session.get("new", False) or not user_phrase:
        reply_text = "Привет! Я полностью бесплатный разум Кими. Что ты хочешь узнать?"
    else:
        try:
            response = client.chat.completions.create(
                model="kimi-k3", 
                messages=[
                    {"role": "system", "content": "Ты голосовой ассистент Kimi в колонке Маруся. Отвечай кратко, понятно, живым языком, без списков, звездочек и смаликов."},
                    {"role": "user", "content": user_phrase}
                ]
            )
            reply_text = response.choices.message.content
        except Exception:
            reply_text = "Ой, что-то связь с Пекином прервалась. Повтори, пожалуйста."

    return {
        "response": {"text": reply_text, "tts": reply_text, "end_session": False},
        "session": {"session_id": session.get("session_id"), "user_id": session.get("user_id"), "message_id": session.get("message_id")},
        "version": data.get("version")
    }
