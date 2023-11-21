import ebay
import scryfall

def main() -> None:

    # Query Ebay
    ebay_handle = ebay.Ebay(query="mtg blood moon")
    listings = ebay_handle.get_prices()
    for item in listings:
        print("Title:", item["title"])
        print("Price:", item["price"]["value"], item["price"]["currency"])
        print("Item ID:", item["itemId"])
        print("URL:", item["itemWebUrl"])
        print("-" * 30)

    # Query Scryfall
    scryfall_handle = scryfall.Scryfall(query="black lotus")

    for set_name in scryfall_handle.sets:
        print("-" * 30)
        print(f"set name: {set_name}")
        print(f"set code: {scryfall_handle.sets[set_name]}")

if __name__ == "__main__":
    main()