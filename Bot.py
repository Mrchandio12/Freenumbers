import os
from telethon import TelegramClient, events
from collections import defaultdict

# Bot ke liye env variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Channels jahan dono inviter aur invitee ko join hona zaroori hai
REQUIRED_CHANNELS = ["@mr_chandio", "@techworldek"]

# Memory me points store karne ke liye
user_points = defaultdict(int)
invites = {}

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def check_membership(user_id):
    """Check karega ki user required channels me joined hai ya nahi."""
    for channel in REQUIRED_CHANNELS:
        try:
            participant = await client.get_participant(channel, user_id)
            if not participant:
                return False
        except Exception:
            return False
    return True

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    inviter_id = event.sender_id
    if event.is_private:
        args = event.raw_text.split()
        if len(args) > 1:
            ref_code = args[1]
            if ref_code.isdigit() and int(ref_code) != inviter_id:
                invites[event.sender_id] = int(ref_code)
                await event.reply("✅ Invite link se join ho gaye!")
                # Check both inviter and invitee membership
                if await check_membership(inviter_id) and await check_membership(event.sender_id):
                    user_points[int(ref_code)] += 2
                    await event.respond(f"🎉 Aapko 2 points mil gaye! Total: {user_points[int(ref_code)]}")
        else:
            await event.reply(
                f"Salam! Apka invite link: https://t.me/{(await client.get_me()).username}?start={inviter_id}"
            )

@client.on(events.NewMessage(pattern='/points'))
async def points_handler(event):
    await event.reply(f"📊 Aapke total points: {user_points[event.sender_id]}")

print("🤖 Bot is running...")
client.run_until_disconnected()
