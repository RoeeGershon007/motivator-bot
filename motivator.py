
import os
import time
import threading
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# === הגדרות סביבתיות ===
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
TO_PHONE_NUMBER = os.environ.get("TO_PHONE_NUMBER")  # מספר ה-WhatsApp של המשתמש
GOOGLE_SHEET_NAME = "Motivator Tracker"

# === חיבור ל-Google Sheets ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).worksheet("Daily Log")

# === Twilio Client ===
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# === Flask ===
app = Flask(__name__)

# === משתנים זמניים למעקב ===
last_prompt_time = None
user_responded = False

# === שליחת תזכורת בוקר ===
def send_morning_reminder():
    global last_prompt_time, user_responded
    message = (
        "🌞 בוקר טוב! תזכורת יומית:\n"
        "- שתית מים?\n- לקחת ויטמין D + B12?\n- לקחת קריאטין?\n- אכלת חלבון?\nענה כן/לא או פרט."
    )
    twilio_client.messages.create(
        from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
        to=f"whatsapp:{TO_PHONE_NUMBER}",
        body=message
    )
    last_prompt_time = time.time()
    user_responded = False

    # הפעלת נודניק לאחר 15 דקות אם אין תגובה
    threading.Timer(900, send_nudge_if_no_response).start()

# === נודניק ===
def send_nudge_if_no_response():
    if not user_responded:
        twilio_client.messages.create(
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=f"whatsapp:{TO_PHONE_NUMBER}",
            body="🔔 היי! רק מזכירים לבדוק אם ביצעת את המשימות של הבוקר."
        )

# === Webhook לתגובות WhatsApp ===
@app.route("/webhook", methods=["POST"])
def webhook():
    global user_responded
    incoming_msg = request.form.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()

    # תיעוד בגיליון Google Sheets
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now, incoming_msg]
    sheet.append_row(row)

    msg.body("📋 תודה! קלטתי את העדכון שלך. נרשם ביומן.")
    user_responded = True
    return str(response)

# === Route להפעלת התזכורת ידנית מ-cron-job ===
@app.route("/send_reminder", methods=["GET"])
def manual_reminder():
    send_morning_reminder()
    return "Reminder sent", 200

# === הפעלת השרת ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
