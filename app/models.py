from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    priority    = Column(String(10), nullable=False)
    status      = Column(String(20), nullable=False, default="abierto")
    assigned_to = Column(String(100), default="Sin asignar")
    created_at  = Column(DateTime, default=datetime.now)
    updated_at  = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    history  = relationship("TicketHistory", back_populates="ticket", cascade="all, delete")
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete")


class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id         = Column(Integer, primary_key=True, index=True)
    ticket_id  = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    field      = Column(String(50), nullable=False)
    old_value  = Column(String(200))
    new_value  = Column(String(200))
    changed_at = Column(DateTime, default=datetime.now)
    note       = Column(String(300))

    ticket = relationship("Ticket", back_populates="history")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"

    id         = Column(Integer, primary_key=True, index=True)
    ticket_id  = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    sender     = Column(String(20), nullable=False)
    content    = Column(Text, nullable=False)
    sentiment  = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)

    ticket = relationship("Ticket", back_populates="messages")