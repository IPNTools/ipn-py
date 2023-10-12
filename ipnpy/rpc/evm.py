from typing import Optional, Union
from web3 import Web3
from contracts.eth.token import ERC20
from rpc.enums import RpcUrl
from exceptions import ConnectionError


class EvmJsonRPC:
    def __init__(self, rpc_url: Optional[Union[RpcUrl, str]]) -> None:
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
                          amount: int) -> str:
        """
        Using the transfer, sends the native currency to another address

        :param private_key: private key from the wallet
        :param from_address: sender's wallet address
        :param to_address: recipient's wallet address
        :param amount: the amount of currency being transferred
        :return: address transaction
        """
        valid_from_address = self._w3.to_checksum_address(from_address)
        nonce = self._w3.eth.get_transaction_count(valid_from_address, 'pending')

        transaction_info = {
            'chainId': self._w3.eth.chain_id,
            'from': valid_from_address,
            'to': self._w3.to_checksum_address(to_address),
            'value': amount,
            'nonce': nonce,
            'gasPrice': self._w3.eth.gas_price,
            'gas': 21000,
        }

        signed_transaction = self._w3.eth.account.sign_transaction(transaction_info, private_key)
        send = self._w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        return send.hex()
