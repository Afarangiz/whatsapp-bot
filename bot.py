from fastapi import FastAPI, Request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = FastAPI()

# Подставь свой API-ключ OpenAI
openai.api_key = "ТВОЙ_OPENAI_API_КЛЮЧ"

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    user_message = form_data.get("Body")
    
    # Отправляем сообщение в ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Ты помощник школы."},
                  {"role": "user", "content": user_message}]
    )

    chatgpt_reply = response["choices"][0]["message"]["content"]

    # Создаём ответ для WhatsApp
    twilio_response = MessagingResponse()
    twilio_response.message(chatgpt_reply)
    
    return str(twilio_response)
