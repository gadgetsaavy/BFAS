from web3 import Web3
from solcx import compile_source

class ContractDeployer:
    def __init__(self, web3_provider, private_key, address):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.private_key = private_key
        self.address = address

    def compile_contract(self, contract_source):
        """
        Compiles the Solidity contract from the source code.
        """
        compiled = compile_source(contract_source)
        return compiled['<stdin>:MyContract']  # Replace 'MyContract' with actual contract name

    def deploy_contract(self, contract_source):
        """
        Deploy the contract to the Ethereum network.
        """
        compiled_contract = self.compile_contract(contract_source)
        contract_abi = compiled_contract['abi']
        contract_bytecode = compiled_contract['bin']

        contract = self.web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

        # Prepare transaction for deployment
        transaction = contract.constructor().buildTransaction({
            'from': self.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('20', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.address),
        })

        # Sign and send the transaction
        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Wait for the transaction receipt to get the contract address
        txn_receipt = self.web3.eth.waitForTransactionReceipt(txn_hash)
        contract_address = txn_receipt.contractAddress
        return contract_address

# Example usage:
contract_source = """
pragma solidity ^0.8.0;

contract MyContract {
    // Contract code here
}
"""
deployer = ContractDeployer(web3_provider="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID", private_key="YOUR_PRIVATE_KEY", address="YOUR_ADDRESS")
contract_address = deployer.deploy_contract(contract_source)
print(f"Contract deployed at address: {contract_address}")
