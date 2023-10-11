import json
from web3 import Web3
from contracts.eth.abi import ERC20_ABI


class ERC20:
    def __init__(self, w3: Web3, contract_address: str) -> None:
        """
        A base class for interacting with contracts implementing the ERC20 interface

        :param w3: Web3 client
        :param contract_address: token contract address implementing the ERC20 interface
        """
        self.contract_address = w3.to_checksum_address(contract_address)
        self._w3 = w3
        self._contract = self._w3.eth.contract(self.contract_address, abi=json.loads(ERC20_ABI))
        self._functions = self._contract.functions

    def get_decimals(self) -> int:
        return self._functions.decimals().call()

    def transfer(self,
                 private_key: str,
                 from_address: str,
                 to_address: str,
                 amount: int) -> str:
        """
        Using the transfer, sends the ERC20 token to another address

        :param private_key: private key from the wallet
        :param from_address: sender's wallet address
        :param to_address: recipient's wallet address
        :param amount: the amount of currency being transferred
        :return: address transaction
        """

        valid_address = self._w3.to_checksum_address(from_address)
        nonce = self._w3.eth.get_transaction_count(valid_address, 'pending')

        transaction_info = {
            'chainId': self._w3.eth.chain_id,
            'gas': 1_000_000,
            'gasPrice': self._w3.eth.gas_price,
            'nonce': nonce,
            'from': valid_address,
        }

        transaction = (
            self._functions.transfer(self._w3.to_checksum_address(to_address), amount)
            .build_transaction(transaction_info)
        )

        signed_transaction = self._w3.eth.account.sign_transaction(transaction, private_key)
        send = self._w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return send.hex()

    def balance_of(self, address: str) -> int:
        """
        Get the balance of the ERC20 token in the EVM network.

        :param address: wallet address
        :return: the balance of the selected wallet
        """
        return self._functions.balanceOf(address).call()
