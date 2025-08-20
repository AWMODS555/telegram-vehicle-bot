import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

ARYA_API_URL = "https://ping.arya.ai/api/v2/rc-verification"
ARYA_API_TOKEN = os.getenv("cd76fb99a76466c1a62fe0b54e82ac4d")
TELEGRAM_TOKEN = os.getenv("8434873232:AAESLjxNt2SskEk0CfqHhU9TYCfD8yBTVYY")

def get_vehicle_details(vehicle_number):
    headers = {"token": ARYA_API_TOKEN, "content-type": "application/json"}
    payload = {"vehicle_number": vehicle_number, "req_id": "unique_123"}
    try:
        response = requests.post(ARYA_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            details = data.get("data", {})
            return {
                "Vehicle Number": details.get("vehicle_number", "N/A"),
                "Chassis": details.get("chassis_number", "N/A"),
                "Engine": details.get("engine_number", "N/A"),
                "Date of Registration": details.get("registration_date", "N/A"),
                "Date of Expiry": details.get("expiry_date", "N/A"),
                "Owner Name": details.get("owner_name", "N/A"),
                "Mobile Numbers": details.get("mobile_number", "N/A")
            }
        else:
            return {"error": data.get("message", "Failed to fetch details")}
    except requests.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Vehicle number bhejo, details launga.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vehicle_number = update.message.text.strip()
    await update.message.reply_text(f"Checking details for: {vehicle_number}...")
    details = get_vehicle_details(vehicle_number)
    if "error" in details:
        await update.message.reply_text(f"Error: {details['error']}")
    else:
        response = (
            f"Vehicle Number: {details['Vehicle Number']}\n"
            f"Chassis: {details['Chassis']}\n"
            f"Engine: {details['Engine']}\n"
            f"Date of Registration: {details['Date of Registration']}\n"
            f"Date of Expiry: {details['Date of Expiry']}\n"
            f"Owner Name: {details['Owner Name']}\n"
            f"Mobile Numbers: {details['Mobile Numbers']}"
        )
        await update.message.reply_text(response)

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()