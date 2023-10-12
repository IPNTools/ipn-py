from enum import Enum


class WebhookEventType(Enum):
    NATIVE = "NT"
    APPROVAL = "AP"
    TRANSFER = "TR"
    DEPOSIT = "DP"
    WITHDRAWAL = "WD"
    CUSTOM = "CU"

    def __str__(self) -> str:
        return self.value
