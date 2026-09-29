from datetime import datetime,timezone
from typing import Optional
from sqlalchemy import String,Text,DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Ticket(Base):
    __tablename__="tickets"
    id: Mapped[int]=mapped_column(primary_key=True,index=True)
    title: Mapped[str]=mapped_column(String(200))
    description: Mapped[str]=mapped_column(Text)
    product: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    channel: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    category: Mapped[Optional[str]]=mapped_column(
        String(50),
        nullable=True
    )
    priority: Mapped[Optional[str]]=mapped_column(
        String(20),
        nullable=True
    )
    status: Mapped[str]=mapped_column(
        String(20),
        default="open"
    )
    created_at: Mapped[datetime]=mapped_column(
        DateTime,
        default=utcnow
    )
    updated_at: Mapped[datetime]=mapped_column(
        DateTime,
        default=utcnow,
        onupdate=utcnow
    )