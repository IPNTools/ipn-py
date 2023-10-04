import json

from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.tron import TAddress

from contracts.tron.abi import TRC20_ABI


class TRC20:
    def __init__(self, client: Tron, contract_address: str | TAddress) -> None:
        """
        A base class for interacting with contracts implementing the TRC20 interface

        :param client: tron client
        :param contract_address: token contract address implementing the TRC20 interface
        """
        self.contract_address = contract_address
        self._client = client
        self._contract = self._client.get_contract(self.contract_address)
        self._contract.abi = json.loads(TRC20_ABI)
        self._functions = self._contract.functions

    def get_decimals(self) -> int:
        return self._functions.decimals()

    def transfer(self,
                 private_key: str,
                 from_address: str,
                 to_address: str,
                 amount: int) -> str:
        """
        Using the transfer, sends the TRC20 token to another address

        :param private_key: private key from the wallet
        :param from_address: sender's wallet address
        :param to_address: recipient's wallet address
        :param amount: the amount of currency being transferred
        :return: address transaction
        """

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
        """
        Get the balance of the TRC20 token in the tron network.

        :param address: wallet address
        :return: the balance of the selected wallet
        """
        return self._functions.balanceOf(address)
