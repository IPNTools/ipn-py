import json
from typing import Optional
from web3 import Web3
from contracts.eth.token import ERC20
from enums import RPC_URL
from exceptions import ConnectionError


ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')


class EvmJsonRPC:
    def __init__(self, rpc_url: Optional[RPC_URL | str]) -> None:
        """
        A class for interacting with EVM networks. You can use the RPC_URL class to connect, or take the address for
        example https://chainlist.org

        :param rpc_url: the address to connect to the RPC.
        """
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        if web3.is_connected():
            self._w3 = web3
        else:
            raise ConnectionError('Error connecting')

    def get_erc20_balance(self,
                          address: str,
                          contract_address: str,
                          raw: bool = False
                          ) -> float:
        """
        Get the balance of the ERC20 token in the EVM network.

        :param address: wallet address
        :param contract_address: token contract address implementing the ERC20 interface
        :param raw: if True, the function returns the balance in the minimum unit of measurement of the currency
        :return: float: the balance of the selected wallet
        """
        erc20 = ERC20(self._w3, contract_address)
        balance = erc20.balance_of(address)

        if not raw:
            decimals = erc20.get_decimals()
            balance /= 10 ** decimals

        return balance

    def get_native_balance(self,
                           address: str,
                           raw: bool = False
                           ) -> float:
        """
        Get the native balance in EVM network

        :param address: Wallet address
        :param raw: If True, the function returns the balance in the minimum unit of measurement of the currency
        :return: the native balance of the selected wallet
        """
        balance = self._w3.eth.get_balance(self._w3.to_checksum_address(address))
        if not raw:
            balance /= 10 ** 18
        return balance

    def send_erc20_token(self,
                         private_key: str,
                         from_address: str,
                         to_address: str,
                         amount: int,
                         contract_address: str) -> str:
        """
        Using the transfer, sends the ERC20 token to another address

        :param private_key: private key from the wallet
        :param from_address: sender's wallet address
        :param to_address: recipient's wallet address
        :param amount: the amount of currency being transferred
        :param contract_address: token contract address implementing the ERC20 interface
        :return: address transaction
        """
        erc20 = ERC20(self._w3, contract_address)
        send = erc20.transfer(private_key, from_address, to_address, amount)
        return send

    def send_native_token(self,
                          private_key: str,
                          from_address: str,
                          to_address: str,
                          amount: float) -> str:
        """
        Using the transfer, sends the native currency to another address

        :param private_key: private key from the wallet
        :param from_address: sender's wallet address
        :param to_address: recipient's wallet address
        :param amount: the amount of currency being transferred
        :return: address transaction
        """
        transaction = self._build_native_transaction(from_address=from_address,
                                                     to_address=to_address,
                                                     amount=amount,
                                                     )

        signed_transaction = self._w3.eth.account.sign_transaction(transaction, private_key)
        send = self._w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return send.hex()
