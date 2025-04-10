from flask import Flask, request
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

app = Flask(__name__)

# הגדרות
GOOGLE_SHEET_NAME = "Motivator Tracker"
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_FROM = "whatsapp:+14155238886"
TWILIO_TO = "whatsapp:+972501234567"  # לשנות למספר שלך

# חיבור לגוגל שיטס
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

def send_whatsapp_message(body):
    client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client_twilio.messages.create(
        from_=TWILIO_FROM,
        body=body,
        to=TWILIO_TO
    )
    return message.sid

@app.route("/send_reminder", methods=["GET"])
def send_reminder():
    try:
        now = datetime.now()
        sheet = client.open(GOOGLE_SHEET_NAME).worksheet("Daily Log")
        sheet.append_row([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), "Reminder Sent", "No"])
        return "Reminder logged successfully."
    except Exception as e:
        return f"Error: {e}"

@app.route("/send_nudge", methods=["GET"])
def send_nudge():
    try:
        sheet = client.open(GOOGLE_SHEET_NAME).worksheet("Daily Log")
        data = sheet.get_all_records()
        if data:
            last_row = data[-1]
            responded = last_row.get("Responded", "Yes")
            if responded.lower() != "yes":
                message = "היי! לא ראינו שענית לתזכורת של הבוקר 😅 שתית מים? לקחת ויטמינים? כתבת בתיעוד?"
                send_whatsapp_message(message)
                now = datetime.now()
                sheet.append_row([
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                    "Nudge Sent",
                    ""
                ])
                return "Nudge sent and logged.", 200
            else:
                return "User already responded – no nudge needed.", 200
        else:
            return "No previous log entry found.", 404
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
