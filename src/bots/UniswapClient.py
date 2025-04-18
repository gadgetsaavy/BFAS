from web3 import Web3
from uniswap import Uniswap
import requests

class UniswapConnector:
    def __init__(self, infura_url, wallet_address, private_key, version=3):
        # Connect to Ethereum node
        self.web3 = Web3(Web3.HTTPProvider(infura_url))

        # Set wallet credentials
        self.address = wallet_address
        self.private_key = private_key

        # Initialize Uniswap client
        self.uniswap = Uniswap(
            address=self.address,
            private_key=self.private_key,
            provider=self.web3,
            version=version
        )

    def get_price(self, token_in, token_out):
        # Fetches token price from Uniswap
        return self.uniswap.get_price_input(token_in, token_out, 1 * 10**18)

    def swap_tokens(self, token_in, token_out, amount_in_wei):
        # Executes token swap
        return self.uniswap.make_trade(token_in, token_out, amount_in_wei)

    def fetch_liquidity_from_router(self, router_url, token_1, token_2):
        """
        Dynamically fetches liquidity from a remote router API endpoint.
        This allows off-chain aggregation of liquidity data before initiating swaps.
        """
        try:
            response = requests.get(
                f'{router_url}/liquidity',
                params={'token_1': token_1, 'token_2': token_2},
                timeout=5
            )
            if response.status_code == 200:
                liquidity_data = response.json()
                return liquidity_data
            else:
                print(f"Failed to fetch liquidity data: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching liquidity: {str(e)}")
            return None

    def choose_best_liquidity(self, router_urls, token_1, token_2):
        """
        Compares liquidity across multiple router URLs and chooses the one with the best available volume.
        """
        best_liquidity = 0
        best_router = None

        for router in router_urls:
            data = self.fetch_liquidity_from_router(router, token_1, token_2)
            if data and 'liquidity' in data:
                liquidity = float(data['liquidity'])
                if liquidity > best_liquidity:
                    best_liquidity = liquidity
                    best_router = router

        return best_router, best_liquidity
