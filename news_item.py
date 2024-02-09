from dataclasses import dataclass


@dataclass
class NewsItem:
    id: str
    title: str
    description: str
    url: str
    image_url: str
    source: str
    author: str
    publish_date: str
