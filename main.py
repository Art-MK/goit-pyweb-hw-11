import logging_config
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from uvicorn.config import LOGGING_CONFIG
import logging

# Uvicorn logging configuration
LOGGING_CONFIG['formatters']['default']['fmt'] = '[%(levelname)s] %(asctime)s "%(message)s"'
LOGGING_CONFIG['formatters']['default']['datefmt'] = '%Y-%m-%d %H:%M:%S'

# file handler for Uvicorn logs
file_handler = logging.FileHandler("./logs/uvicorn.log")
file_handler.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s "%(message)s"', datefmt='%Y-%m-%d %H:%M:%S'))
logging.getLogger("uvicorn").addHandler(file_handler)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "OK"}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the contact API"}

# Endpoint to create a contact
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_contact(db=db, contact=contact)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create contact")

# Endpoint to get all contacts
@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud.get_all_contacts(db=db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to retrieve contacts")

# Endpoint to get a specific contact by ID
@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    try:
        contact = crud.get_contact(db=db, contact_id=contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to retrieve contact")

# Endpoint to update a contact
@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    try:
        updated_contact = crud.update_contact(db=db, contact_id=contact_id, contact=contact)
        if updated_contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return updated_contact
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to update contact")

# Endpoint to delete a contact
@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    try:
        deleted_contact = crud.delete_contact(db=db, contact_id=contact_id)
        if deleted_contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return deleted_contact
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to delete contact")

# Endpoint search contacts
@app.get("/contacts/search/", response_model=list[schemas.Contact])
def search_contacts(
    name: str = None,
    email: str = None,
    db: Session = Depends(get_db)
):
    try:
        return crud.search_contacts(db=db, name=name, email=email)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to search contacts")

# Endpoint get upcoming birthdays
@app.get("/contacts/upcoming_birthdays/", response_model=list[schemas.Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    try:
        return crud.get_contacts_with_upcoming_birthdays(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to retrieve contacts")