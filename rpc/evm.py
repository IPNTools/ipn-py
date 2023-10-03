import json
from typing import Optional
from web3 import Web3
from contracts.eth.token import ERC20
from enums import RPC_URL
from exceptions import CinnectionError

ERC20_ABI = json.loads(
    '''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')


class EvmJsonRPC:
    def __init__(self, rpc_url: Optional[RPC_URL | str]) -> None:
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        if web3.is_connected():
            self._w3 = web3
        else:
            raise CinnectionError('Error connecting')

    def _build_native_transaction(self,
                                  from_address: str,
                                  to_address: str,
                                  amount: float
                                  ) -> dict[str, int | str]:

        gas_price = self._w3.eth.gas_price
        gas = 1_000_000

        nonce = self._w3.eth.get_transaction_count(self._w3.to_checksum_address(from_address), 'pending')

        transaction = {
            'chainId': self._w3.eth.chain_id,
            'from': from_address,
            'to': to_address,
            'value': int(Web3.to_wei(amount, 'ether')),
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas,
        }
        return transaction

    def get_erc20_balance(self,
                          address: str,
                          contract_address: str,
                          raw: bool = False
                          ) -> float:

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

        erc20 = ERC20(self._w3, contract_address)
        send = erc20.transfer(private_key, from_address, to_address, amount)
        return send

    def send_native_token(self,
                          private_key: str,
                          from_address: str,
                          to_address: str,
                          amount: float) -> str:

        transaction = self._build_native_transaction(from_address=from_address,
                                                     to_address=to_address,
                                                     amount=amount,
                                                     )

        signed_transaction = self._w3.eth.account.sign_transaction(transaction, private_key)
        send = self._w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return send.hex()
