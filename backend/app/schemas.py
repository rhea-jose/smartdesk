from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel,ConfigDict,Field

Status=Literal["open",'in_progress','resolved']

class TicketCreate(BaseModel):
    title: str=Field(min_length=3,max_length=200)
    description: str=Field(min_length=5)

class TicketUpdate(BaseModel):
    status: Optional[Status]=None
    category: Optional[str]=None
    priority: Optional[str]=None

class TicketOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    title:str
    description: str
    category: Optional[str]
    priority: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime