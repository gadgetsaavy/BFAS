import pytest
from mev_wrapper import MEVWrapper  # Assuming the MEV wrapper code is in 'mev_wrapper.py'

@pytest.fixture
def setup_mev_wrapper():
    flashbots_url = "https://mev-api-url.com"
    web3_provider = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
    private_key = "YOUR_PRIVATE_KEY"
    address = "YOUR_ADDRESS"
    return MEVWrapper(flashbots_url, web3_provider, private_key, address)

def test_send_mev_bundle(setup_mev_wrapper):
    transaction_data = {
        'to': '0xRecipientAddress',
        'data': '0xTransactionData',
        'gasLimit': 200000,
        'value': '0xValue',
        'maxFeePerGas': '0xMaxFeePerGas',
        'maxPriorityFeePerGas': '0xMaxPriorityFeePerGas'
    }

    bundle = setup_mev_wrapper.create_bundle(transaction_data)
    response = setup_mev_wrapper.send_to_flashbots(bundle)
    
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "bundle successfully sent" in response.text, f"Failed to send MEV bundle."
