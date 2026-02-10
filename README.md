# Telegram News Bot

A Python-based Telegram bot that automatically fetches and sends news updates. The bot prevents duplicate news posts and supports image sharing with formatted messages.

## Features

- 🔄 Automatic news fetching and posting
- 🖼️ Supports news posts with images
- 📝 HTML formatted messages
- ⏱️ Configurable check intervals
- 🔒 Prevents duplicate news posts
- 🐳 Dockerized for easy deployment
- 🔄 Automatic restart on failure
- 💾 Persistent storage for sent news tracking

## Prerequisites

- Docker
- Docker Compose (optional)
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Chat ID where the news will be sent

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Frogleim/anime-news.git
cd anime-news
```