import requests
from dataclasses import dataclass

@dataclass
class ScryfallConfig:
    query: str
    search_url: str = None

    def get_scryfall_prices(self):
        r = requests.get(self.search_url).json()
        print(r['name'])

    def __post_init__(self):
        if self.search_url is None:
            self.search_url = f"https://api.scryfall.com/cards/named?fuzzy={self.query}"
        pass
