from dataclasses import dataclass
from typing import List


@dataclass
class Wallet:
    private_key: str
    tron_address: str
    eth_address: str


@dataclass
class AddressList:
    name: str
    addresses: List[str]
