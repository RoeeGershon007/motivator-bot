import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip().lower()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg == "התחל":
        msg.body("🔥 ברוך הבא לבוט המוטיבציה שלך! מוכן להתחיל?")
    elif "מים" in incoming_msg:
        msg.body("אל תשכח לשתות מים 💧")
    else:
        msg.body(f"קיבלתי: {incoming_msg}")

    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render נותנת את הפורט כמשתנה סביבה
    app.run(host="0.0.0.0", port=port)
