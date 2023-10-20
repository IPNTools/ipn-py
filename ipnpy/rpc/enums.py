from enum import Enum


class RpcUrl(Enum):
    ULTRON = 'https://ultron-rpc.net'
    HARMONY = '	https://harmony.api.onfinality.io/public'
    GNOSIS = 'https://gnosis.blockpi.network/v1/rpc/public'
    FANTOM = 'https://fantom.publicnode.com'
    POLYGON = 'https://avalanche-c-chain.publicnode.com'
    MATIC = 'https://poly-rpc.gateway.pokt.network'
    ETHEREUM = 'https://rpc.mevblocker.io'
    BINANCE = 'https://bsc-dataseed.binance.org/'
    TRON = 'https://api.trongrid.io/'

    def __str__(self) -> str:
        return self.value
