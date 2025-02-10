from fastapi import FastAPI, Request, Form
import openai
from twilio.rest import Client
import os

app = FastAPI()

# Подключаем OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Подключаем Twilio API
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/whatsapp")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    # Отправляем сообщение в ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Ты помощник школы."},
                  {"role": "user", "content": Body}]
    )
    chatgpt_reply = response["choices"][0]["message"]["content"]

    # Отправляем ответ в WhatsApp
    client.messages.create(
        from_=TWILIO_PHONE_NUMBER,
        to=From,
        body=chatgpt_reply
    )

    return "OK"
