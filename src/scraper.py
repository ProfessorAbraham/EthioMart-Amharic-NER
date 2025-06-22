import asyncio
import nest_asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
import emoji
import re
import pandas as pd

nest_asyncio.apply()

def is_amharic(text):
    return any('\u1200' <= c <= '\u137F' for c in text)

async def scrape_telegram_channel(channel_username, client):
    async with client:
        try:
            entity = await client.get_entity(channel_username)
            channel = await client.get_entity(PeerChannel(entity.id))
            print(f"✅ Connected to {channel.title}")

            messages = []
            async for message in client.iter_messages(channel, limit=50):
                if message.text:
                    cleaned_text = clean_amharic_text(message.text)
                    if is_amharic(cleaned_text):
                        messages.append({
                            "channel": channel_username,
                            "raw_text": message.text,
                            "cleaned_text": cleaned_text,
                            "date": message.date.isoformat()
                        })

            print(f"📥 Scraped {len(messages)} Amharic messages from {channel_username}")
            return messages

        except Exception as e:
            print(f"❌ Error scraping {channel_username}: {e}")
            return []

def clean_amharic_text(text):
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\b\d{8,}\b', '', text)
    text = re.sub(r'[^\u1200-\u137F\s\d\.,]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def run_scraper():
    api_id = '21270945'
    api_hash = '369c85ad0099932d4b35b4a44bb86720'
    client = TelegramClient('session_name', api_id, api_hash)

    channels = [
        "shageronlinestore",  # Sample Ethiopian e-commerce channel
        "heyonlinemarket",
        "shilngie",    # Replace with real ones
        "freeonlineshopping2",
        "huluorder",
        "sketmartall",
        "shegersalesman1",
        "ethiooomart",
        "ethio443",
        "betiyegroup",
        "ethio_online_mart",
        "shegerbuyamdsells",
        "shegermarket21",
        "ShegerMarketplace",
        "shegercarmarket",
        "GechoCarMarkeat",
        "Ethiopiaonlin19"
    ]

    all_messages = []
    for chan in channels:
        result = asyncio.get_event_loop().run_until_complete(scrape_telegram_channel(chan, client))
        all_messages.extend(result)

    if all_messages:
        df = pd.DataFrame(all_messages)
        df.to_csv("data/telegram_scraped.csv", index=False)
        print("✅ Saved scraped messages to data/telegram_scraped.csv")
    else:
        print("⚠️ No messages were scraped.")
