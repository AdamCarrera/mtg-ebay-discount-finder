import ebay
import scryfall

def main() -> None:
    ebay_handle = ebay.EbayConfig()
    ebay_handle.get_prices()

    scryfall_handle = scryfall.ScryfallConfig(query="")
    print(scryfall_handle.search_url)
    scryfall_handle.get_scryfall_prices()

if __name__ == "__main__":
    main()