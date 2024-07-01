from pydantic import BaseModel
from typing import Optional


class AdditionalLimit(BaseModel):
    additionalLimitBeginDate: Optional[str] = None
    additionalLimitEndDate: Optional[str] = None
    valueOfAdditionalLimit: Optional[int] = None
    additionalDrugListId: Optional[int] = None
    limitPriority: Optional[str] = None
    additionalLimitId: Optional[int] = None
    kindOfChange: Optional[str] = None


class CardPayload(BaseModel):
    numOfCards: int
    programVariant: str
    programId: int
    activationDateTime: Optional[str] = None
    valueLimit: Optional[int] = None
    realExpiryDate: Optional[str] = None
    productionExpiryDate: Optional[str] = None
    additionalLimit: AdditionalLimit = None
