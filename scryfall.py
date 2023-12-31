from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
from fuzzywuzzy import fuzz
import requests
import json
import re


class OPTIONS(Enum):
    SET = 'SET'
    NAME = 'NAME'

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
            self.search_url = f"https://api.scryfall.com/cards/named"

        # Define default dict of sets and set codes
        if self.sets is None:
            r = requests.get("https://api.scryfall.com/sets/").json()['data']
            self.sets = {item['name']: item['code'] for item in r}
            
            # People typically only call out 'secret lair' in their listings
            self.sets['Secret Lair'] = 'SLD'

        # Define default list of card names
        if self.names is None:
            with open('bulk-data\\oracle-cards-20231121220145.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            self.names = [item['name'] for item in data]


    def scryfall_search_parameters(self, set_name: str, query: str) -> Dict:
        """Define scryfall API parameters"""

        # set_code = set_name_to_set_code(set)
        params = {
            "fuzzy": f"{query}",
            "set": f"{self.sets[set_name]}"
        }
        return params
    

    # def set_name_to_set_code(self, name: str) -> str:
    #     return self.sets[name]
            

    def named_query(self, name, set):
        # Make the request
        response = requests.get(self.search_url, params=self.scryfall_search_parameters(set_name=set, query=name))

        # Check if the request was successful

        if response.status_code == 200:

            data = response.json()

            print('-'*30)
            print(data['name'])
            print(f"Set: {data['set_name']}")
            print(f"Market Price: {data['prices']['usd']}")

            result = {
                "name": data['name'],
                "set": data['set_name'],
                "market_price": data['prices']['usd']
            }

            return result
        

    def to_collector_number(self, name, set):
        pass

    def parse_listing(self, listing: str, option: OPTIONS) -> list:
        """Use regular expressions to parse through a eBay listing to find
        card and set names

        Args:
            listing (str): eBay listing title
            option (OPTIONS): enum to switch between matching set names and matching card names

        Returns:
            list: a list of matches
        """

        if option == OPTIONS.SET:
            patterns = [r"\b" + re.escape(name) + r"\b" for name in self.sets.keys()]
        elif option == OPTIONS.NAME:
            patterns = [r"\b" + re.escape(name) + r"\b" for name in self.names]

        pattern = "|".join(patterns)

        matches = re.findall(pattern, listing, flags=re.IGNORECASE)

        return matches
    
    def parse_listing_fuzzy(self, listing: str) -> list:
        """Use fuzzy logic to find set names in eBay listings

        Args:
            listing (str): listing title from eBay

        Returns:
            list: a list of matches
        """
        threshold = 70
        matches = []

        for name in self.sets.keys():
            ratio = fuzz.partial_ratio(name.lower(), listing.lower())
            if ratio >= threshold:
                matches.append(name)
        return matches


