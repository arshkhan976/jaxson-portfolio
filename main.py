import telebot
import time

BOT_TOKEN = "8390921472:AAF1uaQSx86atqm4GchkxVMv8LQs8XsHC8A"
ADMIN_ID = 7223361270

bot = telebot.TeleBot(BOT_TOKEN)
user_reports = {}  # {user_id: {"case_id": "CC-IND-XYZ", "status": "Investigation Ongoing"}}
case_id_counter = 10001

# ---------- USER SECTION ----------
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "👮‍♂️ Welcome to FraudGuard!\nUse /report to file a scam report.\nUse /status to check your case status.")

@bot.message_handler(commands=['report'])
def report(msg):
    global case_id_counter
    user_id = msg.chat.id
    if user_id not in user_reports:
        case_id = f"CC-IND-{case_id_counter}"
        user_reports[user_id] = {"case_id": case_id, "status": "Investigation Ongoing"}
        case_id_counter += 1
        bot.send_message(user_id, f"✅ Your report has been registered.\n📁 Case ID: {case_id}\n🕵️‍♂️ Status: Investigation Ongoing")
    else:
        bot.send_message(user_id, f"📝 You already have an open case.\n📁 Case ID: {user_reports[user_id]['case_id']}\n📊 Status: {user_reports[user_id]['status']}")

@bot.message_handler(commands=['status'])
def check_status(msg):
    user_id = msg.chat.id
    if user_id in user_reports:
        case = user_reports[user_id]
        bot.send_message(user_id, f"📁 Case ID: {case['case_id']}\n📊 Status: {case['status']}")
    else:
        bot.send_message(user_id, "⚠️ No active case found. Use /report to file one.")

# ---------- ADMIN SECTION ----------
@bot.message_handler(func=lambda msg: msg.chat.id == ADMIN_ID and msg.text.startswith("/broadcast"))
def broadcast(msg):
    text = msg.text.replace("/broadcast ", "")
    for user_id in user_reports:
        try:
            bot.send_message(user_id, f"📢 Admin Alert:\n{text}")
        except:
            pass

@bot.message_handler(func=lambda msg: msg.chat.id == ADMIN_ID and msg.text.startswith("/setstatus"))
def set_status(msg):
    try:
        parts = msg.text.split(" ", 2)
        uid = int(parts[1])
        new_status = parts[2]
        if uid in user_reports:
            user_reports[uid]["status"] = new_status
            bot.send_message(uid, f"📢 Case Update:\n📁 {user_reports[uid]['case_id']}\n📊 New Status: {new_status}")
            bot.send_message(ADMIN_ID, "✅ Status updated.")
        else:
            bot.send_message(ADMIN_ID, "❌ User not found.")
    except:
        bot.send_message(ADMIN_ID, "❌ Format: /setstatus <user_id> <new_status>")

@bot.message_handler(func=lambda msg: msg.chat.id == ADMIN_ID and msg.text.startswith("/reports"))
def all_reports(msg):
    if user_reports:
        report_summary = "\n".join([f"{uid} - {data['case_id']} - {data['status']}" for uid, data in user_reports.items()])
        bot.send_message(ADMIN_ID, f"📋 All Reports:\n{report_summary}")
    else:
        bot.send_message(ADMIN_ID, "📭 No reports found.")

# ---------- MAIN LOOP ----------
def polling_loop():
    while True:
        try:
            bot.polling(non_stop=True, timeout=60)
        except Exception as e:
            print("Bot crashed. Restarting in 10s...", e)
            time.sleep(10)

if __name__ == "__main__":
    polling_loop()
