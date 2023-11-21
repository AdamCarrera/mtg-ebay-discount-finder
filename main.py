import ebay
import scryfall

def main() -> None:

    # Query Ebay
    ebay_handle = ebay.Config(query="blightsteel colossus")

    # Query Scryfall
    scryfall_handle = scryfall.Scryfall(query="black lotus")

    listings = ebay_handle.get_listings()

    for listing in listings:
        print(listing.title)
        print(f"Fuzzy Matches: {scryfall_handle.parse_listing_fuzzy(listing.title)}")
        print(f"Regex Matches: {scryfall_handle.parse_listing(listing.title)}")
        print('-'*30)




if __name__ == "__main__":
    main()