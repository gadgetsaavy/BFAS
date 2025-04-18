# File: /offchain/bot/liquidityaggregator.py

import requests
import logging
from typing import Optional, Dict, List

# Set up logging to track process flow and errors
logging.basicConfig(level=logging.INFO)

class LiquidityAggregator:
    def __init__(self, router_urls: List[str]):
        """
        Initializes the aggregator with a list of DEX router API endpoints.

        :param router_urls: List of base URLs for router APIs (e.g., Uniswap, SushiSwap, etc.)
        """
        self.router_urls = router_urls

    def fetch_liquidity_from_router(self, router_url: str, token_1: str, token_2: str) -> Optional[Dict]:
        """
        Fetch liquidity info for a token pair from a single router API.

        :param router_url: Base URL for the router's API
        :param token_1: Symbol or address of the first token
        :param token_2: Symbol or address of the second token
        :return: Dict with liquidity data or None if request failed
        """
        try:
            response = requests.get(
                f'{router_url}/liquidity',
                params={'token_1': token_1, 'token_2': token_2},
                timeout=5
            )
            if response.status_code == 200:
                logging.info(f"Liquidity fetched from {router_url} for {token_1}/{token_2}")
                return response.json()
            else:
                logging.warning(f"Non-200 response from {router_url}: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Exception when querying {router_url}: {str(e)}")
            return None

    def aggregate_liquidity(self, token_1: str, token_2: str) -> Dict:
        """
        Aggregates liquidity data from all known router URLs for a given token pair.

        :param token_1: First token (symbol or address)
        :param token_2: Second token (symbol or address)
        :return: Aggregated liquidity dictionary keyed by router URL
        """
        aggregated_data = {}

        for router_url in self.router_urls:
            data = self.fetch_liquidity_from_router(router_url, token_1, token_2)
            if data:
                aggregated_data[router_url] = data

        if not aggregated_data:
            logging.error(f"No liquidity data found for {token_1}/{token_2} across all routers.")
        return aggregated_data


# Example usage block (can be removed/commented in production)
if __name__ == "__main__":
    # List of DEX router APIs (these must be real endpoints or mocked/test APIs)
    dex_routers = [
        "https://api.dex1.example.com",
        "https://api.dex2.example.com",
        "https://api.dex3.example.com"
    ]

    # Tokens to check liquidity for
    token_1 = "WETH"
    token_2 = "DAI"

    # Instantiate aggregator and fetch liquidity data
    aggregator = LiquidityAggregator(dex_routers)
    results = aggregator.aggregate_liquidity(token_1, token_2)

    # Print results to stdout
    for router, data in results.items():
        print(f"Liquidity at {router} for {token_1}/{token_2}: {data}")
