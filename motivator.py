from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

GOOGLE_SHEET_NAME = "Motivator Tracker"
WORKSHEET_NAME = "Daily Log"

def get_today_row():
    sheet = client.open(GOOGLE_SHEET_NAME).worksheet(WORKSHEET_NAME)
    today = datetime.now().strftime("%Y-%m-%d")
    cell = sheet.find(today)
    return cell.row if cell else None

@app.route("/send_reminder", methods=["GET"])
def send_reminder():
    try:
        sheet = client.open(GOOGLE_SHEET_NAME).worksheet(WORKSHEET_NAME)
        now = datetime.now()
        sheet.append_row([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M"),
            "Reminder sent"
        ])
        return "Reminder logged successfully."
    except Exception as e:
        return f"Error: {e}"

@app.route("/send_nudge", methods=["GET"])
def send_nudge():
    try:
        sheet = client.open(GOOGLE_SHEET_NAME).worksheet(WORKSHEET_NAME)
        row = get_today_row()
        if not row:
            now = datetime.now()
            sheet.append_row([
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M"),
                "Nudge sent"
            ])
            return "Nudge logged (no prior entry today)."
        else:
            return "Already responded today, no nudge needed."
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
