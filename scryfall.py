from dataclasses import dataclass
from typing import Dict, List
from fuzzywuzzy import fuzz
import requests
import json
import re

@dataclass
class Scryfall:
    query: str
    search_url: str = None
    sets: Dict = None
    names: List = None

    def get_scryfall_prices(self):
        r = requests.get(self.search_url).json()
        print(f"Name: {r['name']}")
        print(f"Set: {r['set_name']}")
        print(f"EDHRec Rank: {r['edhrec_rank']}")
        print(f"Price: {r['prices']['usd']}")
        print("-" * 30)

    def __post_init__(self):
        # Define default search url
        if self.search_url is None:
            self.search_url = f"https://api.scryfall.com/cards/all/28"

        # Define default dict of sets and set codes
        if self.sets is None:
            r = requests.get("https://api.scryfall.com/sets/").json()['data']
            self.sets = {item['name']: item['code'] for item in r}

        # Define default list of card names
        if self.names is None:
            with open('bulk-data\\oracle-cards-20231121220145.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            self.names = [item['name'] for item in data]
            


    def to_collector_number(self, name, set):
        pass

    def parse_listing(self, listing: str) -> list:
        set_code_pattern = r"\b(" + "|".join(self.sets.values()) + r")\b"

        patterns = [r"\b" + re.escape(name) + r"\b" for name in self.sets.keys()]

        set_name_pattern = "|".join(patterns)

        matches = []

        set_code_matches = re.findall(set_code_pattern, listing, flags=re.IGNORECASE)
        matches.append(set_code_matches)

        set_name_matches = re.findall(set_name_pattern, listing, flags=re.IGNORECASE)
        matches.append(set_name_matches)

        return matches
    
    def parse_listing_fuzzy(self, listing: str) -> list:
        threshold = 70
        matches = []

        # matches = [name for name in self.sets.keys() if fuzz.partial_ratio(name.lower(), listing.lower()) >= threshold]

        for name in self.sets.keys():
            ratio = fuzz.partial_ratio(name.lower(), listing.lower())
            if ratio >= threshold:
                matches.append(name)
        return matches


