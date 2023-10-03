from _decimal import Decimal
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey

from contracts.tron.token import TRC20
from exceptions import CinnectionError


class TronJsonRPC:
    def __init__(self, network: str):
        self._client = Tron(HTTPProvider(endpoint_uri=network))
        if not self.is_connected():
            raise CinnectionError('Error connecting')

    def is_connected(self) -> bool:
        try:
            self._client.get_latest_block()
            return True
        except:
            return False

    def get_erc20_balance(self,
                          address: str,
                          contract_address: str,
                          raw: bool = False) -> float:

        trc20 = TRC20(self._client, contract_address)
        balance = trc20.balance_of(address)

        if not raw:
            decimals = trc20.get_decimals()
            balance /= 10 ** decimals

        return balance

    def get_native_balance(self, address: str, raw: bool = False) -> Decimal:
        balance = self._client.get_account_balance(address)
        if raw:
            balance *= 10 ** 6
        return balance

    def send_erc20_token(self,
                         private_key: str,
                         from_address: str,
                         to_address: str,
                         amount: int,
                         contract_address: str) -> str:

        trc20 = TRC20(self._client, contract_address)
        send = trc20.transfer(private_key, from_address, to_address, amount)
        return send

    def send_native_token(self,
                          private_key: str,
                          from_address: str,
                          to_address: str,
                          amount: int
                          ) -> str:
        transaction = (
            self._client.trx.transfer(from_address, to_address, amount)
            .build()
            .sign(PrivateKey(
                bytes.fromhex(private_key.replace('0x', ''))))
        )

        send = transaction.broadcast()
        return send['txid']
