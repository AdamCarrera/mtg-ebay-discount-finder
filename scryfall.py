import requests
from dataclasses import dataclass

@dataclass
class ScryfallConfig:
    query: str
    search_url: str = None

    def get_scryfall_prices(self):
        r = requests.get(self.search_url).json()
        print("-" * 30)
        print(f"Name: {r['name']}")
        print(f"Set: {r['set_name']}")
        print(f"EDHRec Rank: {r['edhrec_rank']}")
        print(f"Price: {r['prices']['usd']}")
        print("-" * 30)

    def __post_init__(self):
        if self.search_url is None:
            self.search_url = f"https://api.scryfall.com/cards/all/28"

    def to_collector_number(self, name, set):
        pass
