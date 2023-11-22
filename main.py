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
        if listing.asking_price is not None:
            print(f"Asking Price: {listing.asking_price}")
        else:
            print(f"Current Bid: {listing.current_bid}")
            
        print(f"Set Matches: {scryfall_handle.parse_listing(listing.title, option=scryfall.OPTIONS.SET)}")
        print(f"Card Name Matches: {scryfall_handle.parse_listing(listing.title, option=scryfall.OPTIONS.NAME)}")
        print('-'*30)


if __name__ == "__main__":
    main()