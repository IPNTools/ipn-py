from typing import List

import base58
import requests
from eth_account import Account
from eth_utils import encode_hex
from requests import Response

from ipnpy.exceptions import ValidationError, ConnectionError, BadRequestError
from ipnpy.schemes.ipn_api import Wallet, AddressList

API_URL = 'http://94.198.218.9:8100/upd_addr'


class IPNTools:
    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    @staticmethod
    def create_wallet() -> Wallet:
        """
        Create a new wallet

        :return: a dataclass with the parameters of the created wallet
        """
        account = Account.create()

        private_key = encode_hex(account.key)
        eth_address = account.address.lower()

        ascii_address = f"41{eth_address[2:]}"
        tron_address = base58.b58encode_check(bytes.fromhex(ascii_address)).decode("utf-8")
        return Wallet(private_key, tron_address, eth_address)

    def add_address(self, address: str) -> AddressList:
        """
        Add the selected address to the address list

        :param address: address to add to the list
        :return: a dataclass with the parameters of the address list
        """
        body = {
            "address": address,
            "secret_key": self.secret_key
        }

        response = requests.put(API_URL, json=body)
        return self._response_analise(response)

    def delete_address(self, address: str) -> AddressList:
        """
        Delete the selected address from the address list

        :param address: address to remove from the list
        :return: a dataclass with the parameters of the address list
        """
        body = {
            "address": address,
            "secret_key": self.secret_key
        }

        response = requests.delete(API_URL, json=body)
        return self._response_analise(response)

    def replace_address(self, addresses: List[str]) -> AddressList:
        """
        Replaces the entire existing list of addresses with the selected one

        :param addresses: new list of addresses to replace
        :return: a dataclass with the parameters of the address list
        """
        body = {
            "addresses": addresses,
            "secret_key": self.secret_key
        }

        response = requests.post(API_URL, json=body)
        return self._response_analise(response)

    @staticmethod
    def _response_analise(response: Response) -> AddressList:
        if response.ok:
            result = response.json()
            return AddressList(result['name'], result['body'])
        elif response.status_code in [400, 409]:
            raise BadRequestError(response.json()['message'])
        elif response.status_code == 422:
            error = response.json()['detail'][0]
            raise ValidationError(f'In field {error["loc"][1]} error: {error["msg"]}')
        else:
            raise ConnectionError(response.reason)
