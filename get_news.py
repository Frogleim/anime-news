import requests
from dotenv import load_dotenv
import os

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

url = 'https://cr-news-api-service.prd.crunchyrollsvc.com/v1/en-US/widget/topstoriesasidewidget'

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': f'Bearer {BEARER_TOKEN}',
    'origin': 'https://www.crunchyroll.com',
    'priority': 'u=1, i',
    'referer': 'https://www.crunchyroll.com/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

from datetime import datetime

from datetime import datetime, timedelta


def get_recent_news(news_data, max_days=1):
    # Get current time
    current_time = datetime.now()

    # Extract stories from the data
    stories = news_data['stories']

    # Filter and sort stories
    recent_news = []
    for story in stories:
        # Parse the creation timestamp
        created_at = datetime.strptime(story['content']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Check if the story is within the last 24 hours
        time_difference = current_time - created_at
        if time_difference <= timedelta(days=max_days):
            news_item = {
                'headline': story['content']['headline'],
                'date': story['content']['article_date'],
                'created_at': created_at,
                'lead': story['content']['lead'],
                'thumbnail': story['content']['thumbnail']['filename'] if story['content']['thumbnail'] else None,
                'category': story['content']['category'],
                'tags': story['tag_list']
            }
            recent_news.append(news_item)

    # Sort by creation time (newest first)
    recent_news.sort(key=lambda x: x['created_at'], reverse=True)
    return recent_news


def format_time_ago(created_at):
    """Convert timestamp to 'time ago' format"""
    now = datetime.now()
    diff = now - created_at

    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    hours = diff.seconds // 3600
    if hours > 0:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    minutes = (diff.seconds % 3600) // 60
    return f"{minutes} minute{'s' if minutes > 1 else ''} ago"


# Example usage:
if __name__ == "__main__":
    response = requests.get(url, headers=headers)
    news_data = response.json()

    recent_news = get_recent_news(news_data)

    if recent_news:
        print(f"Found {len(recent_news)} news items from the last 24 hours:")
        for i, news in enumerate(recent_news, 1):
            print(f"\n{i}. {news['headline']}")
            print(f"Posted: {format_time_ago(news['created_at'])}")
            print(f"Lead: {news['lead']}")
            if news['category']:
                print(f"Category: {news['category']}")
            if news['tags']:
                print(f"Tags: {', '.join(news['tags'])}")
            print(f"Image URL: {news['thumbnail']}")
            print("-" * 80)
    else:
        print("No news items found from the last 24 hours.")