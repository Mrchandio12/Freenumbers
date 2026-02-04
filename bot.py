import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram import ChatMember
import os

TOKEN = "8296493548:AAEULmktpghxxBH4i0ItMBSHzQZVpBeACGk"
CHANNELS = ["@Mr_chandio", "@mrchandio0", "@mrchandioo"]
REFERRAL_TARGET = 20

# Data save karne ke liye (Simple dictionary)
users_data = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    args = context.args

    # Agar link se aaye hain (referral)
    if args:
        ref_id = int(args[0])
        if ref_id != user_id:
            if ref_id not in users_data:
                users_data[ref_id] = {"refs": 0}
            users_data[ref_id]["refs"] += 1

    if user_id not in users_data:
        users_data[user_id] = {"refs": 0}

    invite_link = f"https://t.me/{context.bot.username}?start={user_id}"
    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}!\n\n"
        f"📢 Invite your friends using this link:\n{invite_link}\n\n"
        f"🎯 You have {users_data[user_id]['refs']} referrals.\n"
        f"Target: {REFERRAL_TARGET} referrals to get a reward."
    )

async def check(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Check if joined all channels
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]:
                await update.message.reply_text(f"❌ Please join {channel} first.")
                return
        except:
            await update.message.reply_text(f"❌ Error checking {channel}.")
            return

    # Check referrals
    if users_data.get(user_id, {}).get("refs", 0) >= REFERRAL_TARGET:
        await update.message.reply_text("🎉 Congratulations! You have earned your number: +123456789")
        users_data[user_id]["refs"] = 0  # Reset after reward
    else:
        await update.message.reply_text(f"ℹ️ You have {users_data[user_id]['refs']} referrals. Keep going!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    app.run_polling()
