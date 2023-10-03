from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.tron import TAddress


class TRC20:
    def __init__(self, client: Tron, contract_address: str | TAddress) -> None:
        self.contract_address = contract_address
        self._client = client
        self._contract = self._client.get_contract(self.contract_address)
        self._functions = self._contract.functions

    def get_decimals(self) -> int:
        return self._functions.decimals()

    def transfer(self,
                 private_key: str,
                 from_address: str,
                 to_address: str,
                 amount: int) -> str:

        transaction = (
            self._functions.transfer(to_address, amount)
            .with_owner(from_address)
            .fee_limit(30_000_000)
            .build()
            .sign(PrivateKey(
                bytes.fromhex(private_key.replace('0x', ''))))
        )

        send = transaction.broadcast()
        return send['txid']

    def balance_of(self, address: str) -> int:
        return self._functions.balanceOf(address)
