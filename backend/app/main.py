from typing import Optional
from fastapi import FastAPI, Depends,HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import models,schemas
from .database import Base,engine,get_db
from pydantic import BaseModel, Field
from . import ml_service

class PredictRequest(BaseModel):
    text: str=Field(min_length=5)

Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI(title="SmartDesk")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/tickets",response_model=schemas.TicketOut,status_code=201)
def create_ticket(payload:schemas.TicketCreate,db:Session=Depends(get_db)):
    predictions=ml_service.predict_ticket(payload.description)
    ticket=models.Ticket(
        **payload.model_dump(),
        category=predictions['category'],
        priority=predictions['priority']
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@app.get('/tickets',response_model=list[schemas.TicketOut])
def list_tickets(status:Optional[str]=None,category: Optional[str] = None,skip: int=0,limit:int = Query(50,le=200),db: Session=Depends(get_db)):
    stmt=select(models.Ticket).order_by(models.Ticket.id.desc())
    if status:
        stmt=stmt.where(models.Ticket.status==status)
    if category:
        stmt = stmt.where(models.Ticket.category == category)
    return db.scalars(stmt.offset(skip).limit(limit)).all()

@app.get('/tickets/{ticket_id}',response_model=schemas.TicketOut)
def get_ticket(ticket_id: int,db:Session=Depends(get_db)):
    ticket=db.get(models.Ticket,ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404,detail="Ticket Not Found")
    return ticket

@app.patch("/tickets/{ticket_id}",response_model=schemas.TicketOut)
def update_ticket(ticket_id:int,payload:schemas.TicketUpdate,db: Session=Depends(get_db)):
    ticket=db.get(models.Ticket,ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404,detail="Ticket Not Found")
    for field,value in payload.model_dump(exclude_unset=True).items():
        setattr(ticket,field,value)
    db.commit()
    db.refresh(ticket)
    return ticket

@app.delete("/tickets/{ticket_id}",status_code=204)
def delete_ticket(ticket_id:int,db : Session=Depends(get_db)):
    ticket=db.get(models.Ticket,ticket_id)
    if ticket is None :
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(ticket)
    db.commit()

@app.post('/predict')
def predict(payload:PredictRequest):
    return ml_service.predict_ticket(payload.text)