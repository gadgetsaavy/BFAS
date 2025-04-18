import pytest
from web3 import Web3

from gas_estimator import GasEstimator  # Assuming the gas estimator code is in 'gas_estimator.py'

@pytest.fixture
def setup_web3():
    web3_provider = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
    return Web3(Web3.HTTPProvider(web3_provider))

def test_gas_estimator(setup_web3):
    gas_estimator = GasEstimator(setup_web3)
    
    transaction_data = {
        'to': '0xRecipientAddress',
        'from': '0xSenderAddress',
        'value': setup_web3.toWei(0.1, 'ether'),
        'data': '0xTransactionData'
    }
    
    gas = gas_estimator.estimate_gas(transaction_data)
    
    assert gas is not None, "Gas estimation failed."
    assert gas > 0, "Estimated gas should be greater than 0."
