import ebay
import scryfall

def main() -> None:

    # Query Ebay
    ebay_handle = ebay.Config(query="blightsteel colossus")

    # Query Scryfall
    scryfall_handle = scryfall.Scryfall(query="")

    listings = ebay_handle.get_listings()

    for listing in listings:
        print("EBAY SEARCH")
        print(listing.title)
        if listing.asking_price is not None:
            print(f"Asking Price: {listing.asking_price}")
        else:
            print(f"Current Bid: {listing.current_bid}")

        set_matches = scryfall_handle.parse_listing(listing.title, option=scryfall.OPTIONS.SET)
        name_matches = scryfall_handle.parse_listing(listing.title, option=scryfall.OPTIONS.NAME)
            
        # print(f"Set Matches: {scryfall_handle.parse_listing(listing.title, option=scryfall.OPTIONS.SET)}")
        # print(f"Card Name Matches: {scryfall_handle.parse_listing(listing.title, option=scryfall.OPTIONS.NAME)}")

        card_data = scryfall_handle.named_query(name=name_matches[0], set=set_matches[0])
        print('-'*30)
        print("SCRYFALL SEARCH")
        print(f"Card Name: {card_data['name']}")
        print(f"Set: {card_data['set']}")
        print(f"Market Price: {card_data['market_price']}")
        print('-'*30)
        print('\n\n\n\n')



if __name__ == "__main__":
    main()