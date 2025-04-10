
import os
from flask import Flask
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

app = Flask(__name__)

GOOGLE_SHEET_NAME = "Motivator Tracker"
TAB_NAME = "Daily Log"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client_gs = gspread.authorize(creds)
sheet = client_gs.open(GOOGLE_SHEET_NAME).worksheet(TAB_NAME)

# הגדרות ל-Twilio
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")
client_twilio = Client(TWILIO_SID, TWILIO_AUTH)

def log_reminder():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    row = [now, "Reminder sent"]
    sheet.append_row(row)

def send_nudge():
    message = client_twilio.messages.create(
        from_=TWILIO_FROM,
        to=TWILIO_TO,
        body="🤖 אל תשכח לרשום אם שתית מים, לקחת ויטמינים, חלבון וקריאטין!"
    )
    return message.sid

@app.route("/send_reminder")
def send_reminder():
    try:
        log_reminder()
        return "Reminder logged successfully."
    except Exception as e:
        return f"Error: {e}"

@app.route("/send_nudge")
def send_nudge_route():
    try:
        sid = send_nudge()
        return f"Nudge sent. SID: {sid}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run()
