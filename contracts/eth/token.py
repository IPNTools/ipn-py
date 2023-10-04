import json

from web3 import Web3

ERC20_ABI = json.loads(
    '''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')


class ERC20:
    def __init__(self, w3: Web3, contract_address: str) -> None:
        """
        A base class for interacting with contracts implementing the ERC20 interface

        :param w3: Web3 client
        :param contract_address: token contract address implementing the ERC20 interface
        """
        self.contract_address = w3.to_checksum_address(contract_address)
        self._w3 = w3
        self._contract = self._w3.eth.contract(self.contract_address, abi=ERC20_ABI)
        self._functions = self._contract.functions

    def _build_erc20_transaction(self, from_address: str) -> dict[str, int | str]:
        """
        A private system function for creating a native transaction

        :param from_address: sender's wallet address
        :return: dictionary with transaction information
        """
        nonce = self._w3.eth.get_transaction_count(self._w3.to_checksum_address(from_address), 'pending')

        transaction = {
            'chainId': self._w3.eth.chain_id,
            'gas': 1_000_000,
            'gasPrice': self._w3.eth.gas_price,
            'nonce': nonce,
            'from': from_address,
        }
        return transaction

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

        transaction = (self._functions.transfer(to_address, amount)
                       .build_transaction(self._build_erc20_transaction(from_address)))

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
