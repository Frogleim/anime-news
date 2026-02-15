import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time
import json


load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SENT_NEWS_FILE = "sent_news.json"


def send_telegram_message(bot_token, chat_id, message, image_url=None):
    base_url = f"https://api.telegram.org/bot{bot_token}"

    try:
        if image_url:
            # Send photo with caption
            send_photo_url = f"{base_url}/sendPhoto"
            params = {
                "chat_id": chat_id,
                "photo": image_url,
                "caption": message,
                "parse_mode": "HTML"  # Enable HTML formatting
            }
            response = requests.post(send_photo_url, params=params)
        else:
            # Send text message
            send_message_url = f"{base_url}/sendMessage"
            params = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"  # Enable HTML formatting
            }
            response = requests.post(send_message_url, params=params)

        if response.status_code == 200:
            return True
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(f"Response: {response.json()}")
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


def get_recent_news(news_data, max_days=1):
    current_time = datetime.now()
    stories = news_data['stories']

    recent_news = []
    for story in stories:
        created_at = datetime.strptime(story['content']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        time_difference = current_time - created_at

        if time_difference <= timedelta(days=max_days):
            news_item = {
                'headline': story['content']['headline'],
                'lead': story['content']['lead'],
                'created_at': created_at,
                'thumbnail': story['content']['thumbnail']['filename'] if story['content']['thumbnail'] else None,
                'category': story['content']['category'],
                'tags': story['tag_list']
            }
            recent_news.append(news_item)

    recent_news.sort(key=lambda x: x['created_at'], reverse=True)
    return recent_news


def format_news_message(news_item):
    """Format news item into HTML message"""
    message = f"<b>{news_item['headline']}</b>\n\n"
    message += f"{news_item['lead']}\n\n"

    if news_item['category']:
        message += f"Category: {news_item['category']}\n"
    if news_item['tags']:
        message += f"Tags: {', '.join(news_item['tags'])}\n"

    return message


def load_sent_news():
    """Load previously sent news from JSON file"""
    try:
        if os.path.exists(SENT_NEWS_FILE):
            with open(SENT_NEWS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading sent news: {e}")
        return {}


def save_sent_news(sent_news):
    """Save sent news to JSON file"""
    try:
        with open(SENT_NEWS_FILE, 'w') as f:
            json.dump(sent_news, f)
    except Exception as e:
        print(f"Error saving sent news: {e}")


def cleanup_old_news(sent_news, max_age_days=7):
    """Remove entries older than max_age_days"""
    current_time = datetime.now()
    cleaned_news = {}

    for headline, timestamp in sent_news.items():
        sent_date = datetime.fromisoformat(timestamp)
        if current_time - sent_date <= timedelta(days=max_age_days):
            cleaned_news[headline] = timestamp

    return cleaned_news


def send_news_updates():
    url = 'https://cr-news-api-service.prd.crunchyrollsvc.com/v1/en-US/widget/topstoriesasidewidget'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    try:
        # Load previously sent news
        sent_news = load_sent_news()

        # Cleanup old entries
        sent_news = cleanup_old_news(sent_news)

        response = requests.get(url, headers=headers)
        print(response.json())
        news_data = response.json()
        recent_news = get_recent_news(news_data)

        if recent_news:
            news_sent = False
            for news in recent_news:
                headline = news['headline']

                # Check if news was already sent
                if headline not in sent_news:
                    message = format_news_message(news)
                    success = send_telegram_message(
                        TOKEN,
                        CHAT_ID,
                        message,
                        news['thumbnail']
                    )

                    if success:
                        print(f"Sent news: {headline[:50]}...")
                        # Mark as sent with timestamp
                        sent_news[headline] = datetime.now().isoformat()
                        news_sent = True
                    time.sleep(1)
                else:
                    print(f"Skipping already sent news: {headline[:50]}...")

            if news_sent:
                # Save updated sent news only if we sent something new
                save_sent_news(sent_news)
            elif not news_sent:
                print("All recent news have already been sent")
        else:
            print("No recent news found")

    except Exception as e:
        print(f"Error fetching or sending news: {str(e)}")


if __name__ == "__main__":
    import random
    while True:
        send_news_updates()
        print(f"Waiting for next check... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        time.sleep(3600 * random.randint(7, 22))  # Check every hour instead of every day