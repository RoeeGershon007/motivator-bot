
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from twilio.rest import Client
import os

app = Flask(__name__)

# הגדרות קבועות
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"
GOOGLE_SHEET_NAME = "Motivator Tracker"
TAB_NAME = "Daily Log"

# Twilio - משתנים מתוך Environment
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")
USER_PHONE = os.getenv("USER_PHONE")

# חיבור לגוגל שיטס
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client_gs = gspread.authorize(creds)
sheet = client_gs.open(GOOGLE_SHEET_NAME).worksheet(TAB_NAME)

# שליחת הודעה בוואטסאפ
def send_whatsapp_message(body):
    client_twilio = Client(TWILIO_SID, TWILIO_AUTH)
    client_twilio.messages.create(
        from_=TWILIO_FROM,
        body=body,
        to=USER_PHONE
    )

# שליחת תזכורת
@app.route("/send_reminder", methods=["GET"])
def send_reminder():
    now = datetime.now()
    sheet.append_row([
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),
        "Reminder Sent",
        "No"
    ])
    return "Reminder logged successfully."

# שליחת נודניק אם אין תגובה
@app.route("/send_nudge", methods=["GET"])
def send_nudge():
    try:
        records = sheet.get_all_records()
        today = datetime.now().strftime("%Y-%m-%d")
        for row in reversed(records):
            if row["Date"] == today:
                if row.get("Did you respond?", "").lower() not in ["yes", "בוצע"]:
                    send_whatsapp_message("היי! לא ראינו שענית לתזכורת של הבוקר 😅 שתית מים? לקחת ויטמינים? כתבת בתיעוד?")
                    sheet.append_row([
                        today,
                        datetime.now().strftime("%H:%M:%S"),
                        "Nudge Sent",
                        ""
                    ])
                    return "Nudge sent and logged.", 200
                else:
                    return "User already responded – no nudge needed.", 200
        return "No reminder found for today.", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
