from typing import List
from pydantic import BaseModel, Field
from enums import WebhookEventType


class Log(BaseModel):
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
    logs: List[Log]

    def __init__(self, data: dict, **kwargs) -> None:
        super().__init__(**data, **kwargs)



