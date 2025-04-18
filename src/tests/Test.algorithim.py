# File: src/tests/test.algorithm.py

import unittest
from src.bots.bellmanford import bellman_ford

class TestAlgorithm(unittest.TestCase):
    def test_arbitrage_detection(self):
        graph = {
            'WETH': {'DAI': -0.1, 'USDT': -0.2},
            'DAI': {'USDT': -0.1, 'WETH': -0.1},
            'USDT': {'DAI': -0.05, 'WETH': -0.15}
        }
        result = bellman_ford(graph, 'WETH')
        self.assertIsInstance(result, dict)

if __name__ == '__main__':
    unittest.main()
