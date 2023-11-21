import requests
from dataclasses import dataclass
from typing import Dict

@dataclass
class Scryfall:
    query: str
    search_url: str = None
    sets: Dict = None

    def get_scryfall_prices(self):
        r = requests.get(self.search_url).json()
        print(f"Name: {r['name']}")
        print(f"Set: {r['set_name']}")
        print(f"EDHRec Rank: {r['edhrec_rank']}")
        print(f"Price: {r['prices']['usd']}")
        print("-" * 30)

    def __post_init__(self):
        if self.search_url is None:
            self.search_url = f"https://api.scryfall.com/cards/all/28"

        if self.sets is None:
            r = requests.get("https://api.scryfall.com/sets/").json()['data']
            self.sets = {item['name']: item['code'] for item in r}

        

    def to_collector_number(self, name, set):
        pass

    def to_set_code(self, set_name):
        pass
        # for item in r['data']:
        #     print(f"Set name: {item['name']}")
        #     print(f"Set code: {item['code']}")
        #     print("-" * 30)
