from flask import Flask
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime

app = Flask(__name__)

# שימוש ב-Scope ל-Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# התחברות לחשבון השירות
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# התחברות לפי Spreadsheet ID (כמו שהצעת)
spreadsheet = client.open_by_key("1oZnLMppwaSB99cgbe6wJg7YMY3g-1x5wQxQqMemt4Rg")
sheet = spreadsheet.worksheet("Daily Log")

@app.route("/send_reminder")
def send_reminder():
    now = datetime.datetime.now()
    sheet.append_row([
        now.strftime("%Y-%m-%d %H:%M:%S"),
        "Reminder sent"
    ])
    return "Reminder logged successfully."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
