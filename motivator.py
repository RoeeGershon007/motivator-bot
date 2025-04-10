
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# קריאת משתנים מהסביבה
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
TAB_NAME = os.getenv("TAB_NAME")
RECIPIENT_NUMBER = os.getenv("RECIPIENT_NUMBER")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_SID = os.getenv("TWILIO_SID")

# הגדרת הרשאות גישה לגוגל שיטס
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client_gs = gspread.authorize(creds)

# הדפסה לדיבאג
print("Available spreadsheets:")
print([s.title for s in client_gs.openall()])
print("Trying to open sheet:", GOOGLE_SHEET_NAME)
print("Trying to open tab:", TAB_NAME)

# פתיחת הגיליון והטאב
sheet = client_gs.open(GOOGLE_SHEET_NAME).worksheet(TAB_NAME)

# הכנסת שורת תיעוד
today = datetime.now().strftime("%Y-%m-%d %H:%M")
sheet.append_row([today, "Reminder sent"])
print("Reminder logged for", today)
