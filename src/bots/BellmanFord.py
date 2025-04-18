# File: /offchain/bot/bellmanford.py

import math
import logging
from typing import Dict, Tuple, List, Optional

# Set up logger to track events and errors
logging.basicConfig(level=logging.INFO)

class BellmanFordArbitrage:
    def __init__(self, graph: Dict[str, Dict[str, float]]):
        """
        Initialize with a weighted graph where weights are -log(exchange_rate).
        :param graph: Dictionary representing token connections with negative log weights.
        """
        self.graph = graph

    def find_arbitrage(self, start_token: str) -> Optional[List[str]]:
        """
        Executes Bellman-Ford to detect negative cycles (arbitrage opportunities).
        :param start_token: The token to start traversing from
        :return: A list representing arbitrage cycle if found, else None
        """
        # Step 1: Setup distances and predecessors
        distance = {token: float('inf') for token in self.graph}
        predecessor = {token: None for token in self.graph}
        distance[start_token] = 0

        # Step 2: Relax edges repeatedly
        for i in range(len(self.graph) - 1):
            for u in self.graph:
                for v, weight in self.graph[u].items():
                    if distance[u] + weight < distance[v]:
                        distance[v] = distance[u] + weight
                        predecessor[v] = u

        # Step 3: Check for negative-weight cycles
        for u in self.graph:
            for v, weight in self.graph[u].items():
                if distance[u] + weight < distance[v]:
                    logging.info("Arbitrage opportunity detected!")
                    return self.reconstruct_cycle(predecessor, v)

        logging.info("No arbitrage cycle found.")
        return None

    def reconstruct_cycle(self, predecessor: Dict[str, str], start: str) -> List[str]:
        """
        Reconstructs the arbitrage cycle from the predecessor map.
        :param predecessor: Dictionary mapping token to its predecessor
        :param start: Token where a negative cycle was detected
        :return: List of tokens forming the arbitrage cycle
        """
        cycle = [start]
        current = predecessor[start]

        while current not in cycle and current is not None:
            cycle.append(current)
            current = predecessor[current]

        if current:
            cycle.append(current)
            cycle = cycle[cycle.index(current):]  # Trim to only the cycle

        cycle.reverse()
        logging.info(f"Cycle reconstructed: {' -> '.join(cycle)}")
        return cycle


# Example utility to build the graph from exchange rates
def build_graph_from_prices(prices: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Converts a token price graph into a weight graph using -log(rate) for Bellman-Ford.
    :param prices: Raw token exchange rates
    :return: Graph suitable for Bellman-Ford
    """
    graph = {}
    for base in prices:
        graph[base] = {}
        for quote in prices[base]:
            rate = prices[base][quote]
            if rate > 0:
                graph[base][quote] = -math.log(rate)
    return graph


# Example usage block (this will later be replaced by dynamic pricing input)
if __name__ == "__main__":
    # Simulated exchange rates across tokens (token A -> token B = rate)
    prices = {
        'WETH': {'DAI': 3000.0, 'USDT': 2995.0},
        'DAI': {'USDT': 0.998, 'WETH': 0.00033},
        'USDT': {'DAI': 1.002, 'WETH': 0.000334}
    }

    # Build weight graph from exchange rates
    weighted_graph = build_graph_from_prices(prices)

    # Initialize and search for arbitrage cycle
    bf = BellmanFordArbitrage(weighted_graph)
    cycle = bf.find_arbitrage('WETH')

    if cycle:
        print(f"Arbitrage Cycle Found: {' -> '.join(cycle)}")
    else:
        print("No arbitrage cycle found.")
