import os
import requests
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import Dict, List

def defaut_ebay_headers() -> Dict[str, str]:
    """Define default eBay API headers"""
    load_dotenv()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}",        
    }
    
    return headers

def default_ebay_params(query: str) -> Dict:
    """Define default eBay API parameters"""
    params = {
        "q": f"{query}",
        "limit": 5,      # Adjust the number of items you want in the response
        "filter": "buyingOptions:{FIXED_PRICE | AUCTION}"
    }
    return params

@dataclass
class Listing:
    title: str = ""
    set_code: str = ""
    set_name: str  = ""
    market_value: float = 0.00
    asking_price: float = 0.00
    current_bid: float = 0.00
    url: str = ""

@dataclass
class Config:
    """
    Represents a configuration class for eBay API settings.

    Attributes:
    - app_id (str): eBay application ID obtained from the environment variable 'APP_ID'.
    - cert_id (str): eBay certificate ID obtained from the environment variable 'CERT_ID'.
    - access_token (str): eBay API access token obtained from the environment variable 'API_KEY'.
    - query (str): Default query string for eBay search. Defaults to 'laptop'.
    - search_url (str): URL for the eBay Search API endpoint.
    - headers (Dict[str, str]): Request headers for API calls.
    - params (Dict[str, str]): Request parameters for API calls.

    Methods:
    - __init__(): Initializes the class by loading environment variables for default values.
    """
    app_id: str = os.getenv("APP_ID")
    cert_id: str = os.getenv("CERT_ID")
    access_token: str = os.getenv("API_KEY")
    query: str = 'laptop'
    search_url: str = "https://api.ebay.com/buy/browse/v1/item_summary/search"
    headers: Dict[str, str] = field(default_factory=defaut_ebay_headers)
    params: Dict[str, str] = field(default=None)


    def __post_init__(self):
        """load .env file for default values in the class"""
        load_dotenv()
        self.params = default_ebay_params(self.query)
        self.app_id = os.getenv("APP_ID")
        self.cert_id = os.getenv("CERT_ID")
        self.access_token: str = os.getenv("API_KEY")


    def get_listings(self) -> List[Listing]:
        # Make the request
        response = requests.get(self.search_url, headers=self.headers, params=self.params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:

            # The API response is usually in JSON format
            data = response.json()
            # print(data)
            
            # Extract and return relevant information from the response
            if data["total"] <= 0:
                return []
            else:
                return [Listing(
                    title=item['title'], 
                    asking_price=item["price"]["value"] if "price" in item else None,
                    url=item['itemWebUrl'],
                    current_bid=item["currentBidPrice"]["value"] if "currentBidPrice" in item else None
                ) for item in data["itemSummaries"]]
            
        else:
            print("Error:", response.status_code, response.text)

    