from enum import Enum


class WebhookEventType(Enum):
    NATIVE = "NT"
    APPROVAL = "AP"
    TRANSFER = "TR"
    DEPOSIT = "DP"
    WITHDRAWAL = "WD"
    CUSTOM = "CU"