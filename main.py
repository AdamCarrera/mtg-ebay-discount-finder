import ebay
import scryfall

def main() -> None:
    ebay_handle = ebay.EbayConfig(query="mtg blood moon")
    ebay_handle.get_prices()

    scryfall_handle = scryfall.ScryfallConfig(query="black lotus")
    print(scryfall_handle.search_url)
    # scryfall_handle.get_scryfall_prices()
    # scryfall_handle.get_set_codes()

if __name__ == "__main__":
    main()