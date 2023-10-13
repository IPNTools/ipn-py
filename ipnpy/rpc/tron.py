from _decimal import Decimal
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey

from ipnpy.contracts.tron.token import TRC20
from ipnpy.exceptions import ConnectionError


class TronJsonRPC:
    def __init__(self, network: str = 'https://api.shasta.trongrid.io'):
        """
        A class for interacting with tron networks.

        :param network: the address to connect to the RPC. By default, the test network is selected
        """
        self._client = Tron(HTTPProvider(endpoint_uri=network))
        if not self.is_connected():
            raise ConnectionError('Error connecting')

    def is_connected(self) -> bool:
        """
        Сhecks the connection to the RPC
        :return: True if enabled
        """
        try:
            self._client.get_latest_block()
            return True
        except:
            return False

    def get_trc20_balance(self,
                          address: str,
                          contract_address: str,
                          raw: bool = False) -> float:
        """
        Get the balance of the ERC20 token in the tron network.

        :param address: wallet address
        :param contract_address: token contract address implementing the TRC20 interface
        :param raw: if True, the function returns the balance in the minimum unit of measurement of the currency
        :return: float: the balance of the selected wallet
        """
        trc20 = TRC20(self._client, contract_address)
        balance = trc20.balance_of(address)

        if not raw:
            decimals = trc20.get_decimals()
            balance /= 10 ** decimals

        return balance

    def get_native_balance(self, address: str, raw: bool = False) -> Decimal:
        """
        Get the native balance in tron network

        :param address: Wallet address
        :param raw: If True, the function returns the balance in the minimum unit of measurement of the currency
        :return: the native balance of the selected wallet
        """
        balance = self._client.get_account_balance(address)
        if raw:
            balance *= 10 ** 6
        return balance

    def send_trc20_token(self,
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
        :param contract_address: token contract address implementing the TtRC20 interface
        :return: address transaction
        """

        trc20 = TRC20(self._client, contract_address)
        send = trc20.transfer(private_key, from_address, to_address, amount)
        return send

    def send_native_token(self,
                          private_key: str,
                          from_address: str,
                          to_address: str,
                          amount: int
                          ) -> str:
        """
        Using the transfer, sends the native currency to another address

        :param private_key: private key from the wallet
        :param from_address: sender's wallet address
        :param to_address: recipient's wallet address
        :param amount: the amount of currency being transferred
        :return: address transaction
        """
        transaction = (
            self._client.trx.transfer(from_address, to_address, amount)
            .build()
            .sign(PrivateKey(
                bytes.fromhex(private_key.replace('0x', ''))))
        )

        send = transaction.broadcast()
        return send['txid']
