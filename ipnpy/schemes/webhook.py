from typing import List, Union

from pydantic import BaseModel, Field

from ipnpy.schemes.enums import WebhookEventType


class LogERC20(BaseModel):
    from_address: str = Field(..., alias="from")
    to_address: str = Field(..., alias="to")
    value: str
    contract_address: str = Field(..., alias="address")
    topic: str


class LogNative(BaseModel):
    from_address: str = Field(..., alias="from")
    to_address: str = Field(..., alias="to")
    value: str


class Info(BaseModel):
    project: str
    type: WebhookEventType
    rule: str
    amount: int
    date: float
    on_site: bool
    telegram: bool


class WebhookData(BaseModel):
    hash: str
    network: str
    info: Info
    logs: List[Union[LogERC20, LogNative]]

    def __init__(self, data: dict, **kwargs) -> None:
        super().__init__(**data, **kwargs)
