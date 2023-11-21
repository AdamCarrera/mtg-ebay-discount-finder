import ebay
import scryfall

def main() -> None:

    # Query Ebay
    ebay_handle = ebay.Config(query="mtg blood moon")

    # Query Scryfall
    scryfall_handle = scryfall.Scryfall(query="black lotus")

    listings = ebay_handle.get_listings()

    for listing in listings:
        print(listing.title)
        print(scryfall_handle.parse_listing(listing.title))
    



if __name__ == "__main__":
    main()