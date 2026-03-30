from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base, Ticket
from app.routers import tickets

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduLabs Help Desk")

app.include_router(tickets.router)

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "total":      db.query(Ticket).count(),
        "abierto":    db.query(Ticket).filter(Ticket.status == "abierto").count(),
        "en_progreso":db.query(Ticket).filter(Ticket.status == "en_progreso").count(),
        "resuelto":   db.query(Ticket).filter(Ticket.status == "resuelto").count(),
        "cerrado":    db.query(Ticket).filter(Ticket.status == "cerrado").count(),
        "alta":       db.query(Ticket).filter(Ticket.priority == "alta").count(),
        "media":      db.query(Ticket).filter(Ticket.priority == "media").count(),
        "baja":       db.query(Ticket).filter(Ticket.priority == "baja").count(),
    }

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")