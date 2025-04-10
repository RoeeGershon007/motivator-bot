
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Logging helper
def log(msg):
    print(f"[MotivatorBot] {msg}")

log("Starting MotivatorBot...")

# Load environment variables
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
TAB_NAME = os.getenv("TAB_NAME")

log(f"GOOGLE_SHEET_NAME: {GOOGLE_SHEET_NAME}")
log(f"TAB_NAME: {TAB_NAME}")

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client_gs = gspread.authorize(creds)

# Debug available spreadsheets
log("Attempting to list available spreadsheets...")
try:
    available_sheets = client_gs.openall()
    log(f"Available spreadsheets (count: {len(available_sheets)}): {[s.title for s in available_sheets]}")
except Exception as e:
    log(f"Failed to list spreadsheets: {e}")

# Try to access the spreadsheet
try:
    log(f"Trying to open sheet: {GOOGLE_SHEET_NAME}")
    sheet = client_gs.open(GOOGLE_SHEET_NAME).worksheet(TAB_NAME)
    log(f"Successfully opened tab: {TAB_NAME}")
except gspread.SpreadsheetNotFound as e:
    log("SpreadsheetNotFound: The bot could not find the spreadsheet.")
    log(str(e))
except gspread.WorksheetNotFound as e:
    log("WorksheetNotFound: The bot could not find the worksheet/tab.")
    log(str(e))
except Exception as e:
    log(f"Other error occurred while accessing the sheet: {e}")

# Optional: Insert a sample log
try:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, "Test log from updated motivator.py"])
    log("Appended test row successfully.")
except Exception as e:
    log(f"Failed to append row: {e}")
