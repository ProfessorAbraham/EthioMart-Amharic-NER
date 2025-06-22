from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Create Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
    except Exception as e:
        print(f"❌ Failed to get entity for {channel_username}: {e}")
        return

    print(f"📥 Scraping {channel_username}...")
    async for message in client.iter_messages(entity, limit=10000):
        try:
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)

            writer.writerow([
                channel_title,
                channel_username,
                message.id,
                message.message,
                message.date,
                media_path
            ])
        except Exception as e:
            print(f"⚠️ Skipped message {message.id} due to: {e}")

async def main():
    await client.start(phone=phone)

    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    file_exists = os.path.isfile('telegram_data.csv')

    with open('telegram_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header only if the file is new
        if not file_exists:
            writer.writerow([
                'Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'
            ])

        # Add multiple channels here
        channels = [
            '@Shageronlinestore',
            '@shilngie',
            '@heyonlinemarket',
            '@helloomarketethiopia',
            '@huluorder'
        ]

        for channel in channels:
            await scrape_channel(client, channel, writer, media_dir)
            print(f"✅ Finished scraping {channel}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
