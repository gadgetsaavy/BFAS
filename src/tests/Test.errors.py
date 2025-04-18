# File: src/tests/test.errors.py

import unittest

class TestErrorHandling(unittest.TestCase):
    def test_error_trigger(self):
        try:
            raise ValueError("Simulated failure")
        except ValueError as e:
            self.assertEqual(str(e), "Simulated failure")

if __name__ == '__main__':
    unittest.main()
