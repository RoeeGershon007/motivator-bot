from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip().lower()
    resp = MessagingResponse()

    if "התחל" in incoming_msg:
        resp.message("🚀 הבוט שלך מוכן! כתוב 'יומן' או 'תזונה' כדי שנתחיל.")
    elif "תזונה" in incoming_msg:
        resp.message("🍗 מה אכלת היום? כתוב לדוגמה: 2 שיפודי פרגית ו100 גרם אורז.")
    elif "יומן" in incoming_msg:
        resp.message("📅 כתוב לי איך עבר היום שלך ואשמור את זה.")
    else:
        resp.message("🤖 לא הבנתי. נסה: 'התחל', 'תזונה' או 'יומן'.")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
