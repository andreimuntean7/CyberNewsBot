#!/usr/bin/env python3.12

from typing import List
import configparser
import logging
import requests
from classes.ms_teams import MsTeams
from news_item import NewsItem


def get_config() -> configparser.ConfigParser:
    """
    Reads the configuration file and returns a ConfigParser object.
    """
    config = configparser.ConfigParser()
    config.read("./config.cfg")
    return config


def get_latest_news(config: configparser.ConfigParser) -> List[NewsItem]:
    """
    Retrieves the latest news from the source URL specified in the configuration file.

    Args:
        config (ConfigParser): Configuration object containing the source URL and latest index.

    Returns:
        list: List of NewsItem instances representing the latest news items.
    """
    source_url: str = config.get("Variables", "source")
    latest_index: str = config.get("Variables", "latest_index")
    response = requests.get(url=source_url, timeout=5)
    output_news: List[NewsItem] = []
    newer_news: bool = False
    if response.ok:
        news_json = response.json()
        news_json.reverse()
        for item in news_json:
            if newer_news:
                news_item = NewsItem(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"],
                    url=item["url"],
                    image_url=item["image_url"],
                    source=item["source"],
                    author=item["author"],
                    publish_date=item["publish_date"],
                )
                output_news.append(news_item)
            if item["id"] == latest_index:
                newer_news = True
    return output_news


def update_config(
    config: configparser.ConfigParser, latest_news: List[NewsItem]
) -> None:
    """
    Updates the configuration file with the latest news index.

    Args:
        config (ConfigParser): Configuration object.
        latest_news (list): List of NewsItem instances representing the latest news items.
    """
    if latest_news:
        latest_index: str = latest_news[-1].id
        config.set("Variables", "latest_index", latest_index)
        with open("config.cfg", "w", encoding="utf-8") as configfile:
            config.write(configfile)


def print_news(news_list: List[NewsItem]) -> None:
    """
    Prints the news items to the console.

    Args:
        news_list (list): List of NewsItem instances representing the news items.
    """
    for news in news_list:
        print(f"{news}\n")


def main() -> None:
    """
    Main function to retrieve and display the latest news.
    """
    config: configparser.ConfigParser = get_config()
    latest_news: List[NewsItem] = get_latest_news(config)
    update_config(config, latest_news)
    teams = MsTeams()
    for article in latest_news:
        teams.send_message(article=article)


if __name__ == "__main__":
    main()
