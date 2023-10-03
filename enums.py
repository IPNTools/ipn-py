from enum import Enum


class WebhookEventType(Enum):
    NATIVE = "NT"
    APPROVAL = "AP"
    TRANSFER = "TR"
    DEPOSIT = "DP"
    WITHDRAWAL = "WD"
    CUSTOM = "CU"

    def __str__(self):
        return self.value


class RPC_URL(Enum):
    ULTRON = 'https://ultron-rpc.net'
    HARMONY = '	https://harmony.api.onfinality.io/public'
    GNOSIS = 'https://gnosis.blockpi.network/v1/rpc/public'
    FANTOM = 'https://fantom.publicnode.com'
    POLYGON = 'https://avalanche-c-chain.publicnode.com'
    MATIC = 'https://poly-rpc.gateway.pokt.network'
    ETHEREUM = 'https://rpc.mevblocker.io'
    BINANCE = 'https://bsc-dataseed.binance.org/'

    def __str__(self):
        return self.value
