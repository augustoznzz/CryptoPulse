from market_data import MarketDataFetcher

if __name__ == "__main__":
    fetcher = MarketDataFetcher(verbose=True)
    coins = fetcher.get_top_cryptocurrencies(limit=20)
    print(f"Total de moedas retornadas: {len(coins)}")
    for coin in coins:
        print(coin)