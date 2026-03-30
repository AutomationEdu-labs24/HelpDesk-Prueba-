from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Ticket, TicketHistory, TicketMessage
from app.schemas import TicketCreate, TicketUpdate, TicketOut, MessageCreate, MessageOut
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
router = APIRouter(prefix="/api/tickets", tags=["tickets"])

# ── Crear ticket ──────────────────────────────────────
@router.post("", status_code=201, response_model=TicketOut)
def create_ticket(data: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(**data.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    db.add(TicketHistory(
        ticket_id=ticket.id,
        field="status",
        old_value=None,
        new_value="abierto",
        note="Ticket creado"
    ))
    db.commit()
    db.refresh(ticket)
    return ticket

# ── Listar tickets ────────────────────────────────────
@router.get("")
def list_tickets(status: str = None, priority: str = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    return query.order_by(Ticket.created_at.desc()).all()

# ── Detalle de ticket ─────────────────────────────────
@router.get("/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return {
        "ticket":   ticket,
        "history":  ticket.history,
        "messages": ticket.messages
    }

# ── Actualizar ticket ─────────────────────────────────
@router.patch("/{ticket_id}")
def update_ticket(ticket_id: int, data: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    changes = data.model_dump(exclude_unset=True)
    note = changes.pop("note", None)

    for field, new_value in changes.items():
        old_value = str(getattr(ticket, field))
        setattr(ticket, field, new_value)
        db.add(TicketHistory(
            ticket_id=ticket.id,
            field=field,
            old_value=old_value,
            new_value=str(new_value),
            note=note or f"Campo '{field}' actualizado"
        ))

    ticket.updated_at = datetime.now()
    db.commit()
    db.refresh(ticket)
    return ticket

# ── Eliminar ticket ───────────────────────────────────
@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    db.delete(ticket)
    db.commit()
    return {"message": "Ticket eliminado"}

# ── Agregar mensaje ───────────────────────────────────
@router.post("/{ticket_id}/messages", status_code=201)
def add_message(ticket_id: int, data: MessageCreate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    msg = TicketMessage(ticket_id=ticket_id, **data.model_dump())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


# ── IA: análisis de sentimiento ───────────────────────
@router.post("/{ticket_id}/ai/sentiment")
async def analyze_sentiment(ticket_id: int, body: dict, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    text = body.get("text", "")
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 10,
                "system": "Analizador de sentimientos. Responde SOLO con una palabra: positivo, neutral, negativo o molesto.",
                "messages": [{"role": "user", "content": f"Sentimiento de: \"{text}\""}]
            },
            timeout=30
        )
    data = res.json()
    if "content" not in data:
        print("Error Anthropic:", data)
        return {"sentiment": "neutral"}
    sentiment = data["content"][0]["text"].strip().lower().replace(".", "")
    return {"sentiment": sentiment}


# ── IA: generar respuesta ─────────────────────────────
@router.post("/{ticket_id}/ai/suggest")
async def suggest_response(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    messages_text = "\n".join(
        [f"[{m.sender}]: {m.content}" for m in ticket.messages]
    )
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 400,
                "system": "Eres asistente de help desk de EduLabs. Redacta respuestas profesionales y empáticas en español.",
                "messages": [{
                    "role": "user",
                    "content": f"Título: {ticket.title}\nDescripción: {ticket.description}\nPrioridad: {ticket.priority}\nMensajes:\n{messages_text}\n\nRedacta una respuesta para el técnico."
                }]
            },
            timeout=30
        )
    data = res.json()
    if "content" not in data:
        print("Error Anthropic:", data)
        raise HTTPException(status_code=500, detail=str(data))
    suggestion = data["content"][0]["text"].strip()
    return {"suggestion": suggestion}