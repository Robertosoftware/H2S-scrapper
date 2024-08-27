import asyncio
import os

import telegram

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
DEBUGGING_CHAT_ID = os.getenv("DEBUGGING_CHAT_ID")

if TELEGRAM_API_KEY is None:
    print("TELEGRAM_API_KEY not set")
else:
    print(f"TELEGRAM_API_KEY: {TELEGRAM_API_KEY}")

if DEBUGGING_CHAT_ID is None:
    print("DEBUGGING_CHAT_ID not set")
else:
    print(f"DEBUGGING_CHAT_ID: {DEBUGGING_CHAT_ID}")


bot = telegram.Bot(token=TELEGRAM_API_KEY)


async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=DEBUGGING_CHAT_ID)


async def main():
    # Sending a message
    await send_message(text="Hi!, How are you?", chat_id=DEBUGGING_CHAT_ID)


if __name__ == "__main__":
    asyncio.run(main())
