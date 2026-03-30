from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

# ── Ticket ────────────────────────────────────────────
class TicketCreate(BaseModel):
    title:       str
    description: str
    priority:    str
    assigned_to: Optional[str] = "Sin asignar"

    @field_validator("title")
    def title_length(cls, v):
        if len(v.strip()) <= 10:
            raise ValueError("El título debe tener más de 10 caracteres.")
        return v.strip()

    @field_validator("description")
    def description_length(cls, v):
        if len(v.strip()) <= 30:
            raise ValueError("La descripción debe tener más de 30 caracteres.")
        return v.strip()

    @field_validator("priority")
    def priority_valid(cls, v):
        if v not in ("alta", "media", "baja"):
            raise ValueError("Prioridad debe ser: alta, media o baja.")
        return v


class TicketUpdate(BaseModel):
    title:       Optional[str] = None
    description: Optional[str] = None
    priority:    Optional[str] = None
    status:      Optional[str] = None
    assigned_to: Optional[str] = None
    note:        Optional[str] = None

    @field_validator("status")
    def status_valid(cls, v):
        if v and v not in ("abierto", "en_progreso", "resuelto", "cerrado"):
            raise ValueError("Estado inválido.")
        return v

    @field_validator("priority")
    def priority_valid(cls, v):
        if v and v not in ("alta", "media", "baja"):
            raise ValueError("Prioridad inválida.")
        return v


class TicketOut(BaseModel):
    id:          int
    title:       str
    description: str
    priority:    str
    status:      str
    assigned_to: str
    created_at:  datetime
    updated_at:  datetime

    model_config = {"from_attributes": True}


# ── Message ───────────────────────────────────────────
class MessageCreate(BaseModel):
    sender:    str
    content:   str
    sentiment: Optional[str] = None


class MessageOut(BaseModel):
    id:         int
    ticket_id:  int
    sender:     str
    content:    str
    sentiment:  Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}