from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from app.database import create_db_and_tables, get_session
from app.models import ContactMessage, ContactMessageCreate, ContactMessageRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/messages", response_model=ContactMessageRead)
def create_message(data: ContactMessageCreate, session: Session = Depends(get_session)):
    message = ContactMessage.model_validate(data)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@app.get("/messages", response_model=list[ContactMessageRead])
def list_messages(session: Session = Depends(get_session)):
    return session.exec(select(ContactMessage)).all()


@app.get("/messages/{message_id}", response_model=ContactMessageRead)
def get_message(message_id: int, session: Session = Depends(get_session)):
    message = session.get(ContactMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@app.delete("/messages/{message_id}")
def delete_message(message_id: int, session: Session = Depends(get_session)):
    message = session.get(ContactMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    session.delete(message)
    session.commit()
    return {"detail": "deleted"}
