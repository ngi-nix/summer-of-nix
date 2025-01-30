from typing import List, Optional

from pydantic import BaseModel, Field

from models_dashboard import Fund


class Subgrant(BaseModel):
    name: Optional[str] = Field(default=None)
    websites: List[str]
    summary: str
    contact: Fund.Subgrant.Proposal.Contact


class Project(BaseModel):
    name: str = ""
    subgrants: List[str] = []
