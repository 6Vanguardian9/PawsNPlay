from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from dbstruct.database_conn import engine, get_db
import dbstruct.models as models
import dbstruct.schemas as schemas
from pydantic import BaseModel
from worker import process_ingestion


app = FastAPI()

# Create database schema
models.Base.metadata.create_all(bind=engine)


# ------------------- ROOT TEST ROUTE -------------------
@app.get("/")
def root():
    return {"message": "Pet AI Backend Running!"}


# =======================================================
#                    CREATE / POST APIs
# =======================================================

# ------------------- ADD PARENT -------------------
@app.post("/parents", response_model=schemas.ParentResponse)
def add_parent(parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    new_parent = models.Parent(**parent.dict())
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    return new_parent


# ------------------- ADD PET -------------------
@app.post("/pets", response_model=schemas.PetResponse)
def add_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    new_pet = models.Pet(**pet.dict())
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet


# ------------------- ADD PET EVENT -------------------
@app.post("/pet-events", response_model=schemas.PetEventResponse)
def add_pet_event(event: schemas.PetEventCreate, db: Session = Depends(get_db)):
    new_event = models.PetEvent(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


# ------------------- ADD REMINDER -------------------
@app.post("/reminders", response_model=schemas.ReminderResponse)
def add_reminder(reminder: schemas.ReminderCreate, db: Session = Depends(get_db)):
    new_reminder = models.Reminder(**reminder.dict())
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return new_reminder


@app.post("/behavior", response_model=schemas.BehaviorResponse)
def add_behavior(behavior: schemas.BehaviorCreate, db: Session = Depends(get_db)):
    new_behavior = models.Behavior(**behavior.dict())
    db.add(new_behavior)
    db.commit()
    db.refresh(new_behavior)
    return new_behavior



@app.get("/parents/{parent_id}/pets", response_model=list[schemas.PetResponse])
def get_pets_by_parent(parent_id: int, db: Session = Depends(get_db)):
    pets = db.query(models.Pet).filter(models.Pet.parent_id == parent_id).all()
    return pets


@app.get("/pets/{pet_id}/events", response_model=list[schemas.PetEventResponse])
def get_pet_events(pet_id: int, db: Session = Depends(get_db)):
    events = db.query(models.PetEvent).filter(models.PetEvent.pet_id == pet_id).all()
    return events


@app.get("/pets/{pet_id}/reminders", response_model=list[schemas.ReminderResponse])
def get_pet_reminders(pet_id: int, db: Session = Depends(get_db)):
    reminders = db.query(models.Reminder).filter(models.Reminder.pet_id == pet_id).all()
    return reminders


@app.get("/pets/{pet_id}/behavior", response_model=list[schemas.BehaviorResponse])
def get_pet_behavior(pet_id: int, db: Session = Depends(get_db)):
    behavior = db.query(models.Behavior).filter(models.Behavior.pet_id == pet_id).all()
    return behavior


@app.get("/pets/{pet_id}/full", response_model=schemas.PetFullResponse)
def get_full_pet_profile(pet_id: int, db: Session = Depends(get_db)):

    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    events = db.query(models.PetEvent).filter(models.PetEvent.pet_id == pet_id).all()
    reminders = db.query(models.Reminder).filter(models.Reminder.pet_id == pet_id).all()
    behavior = db.query(models.Behavior).filter(models.Behavior.pet_id == pet_id).all()

    return schemas.PetFullResponse.model_validate(
    {
        **pet.__dict__,
        "events": [schemas.PetEventResponse.model_validate(e, from_attributes=True) for e in events],
        "reminders": [schemas.ReminderResponse.model_validate(r, from_attributes=True) for r in reminders],
        "behavior": [schemas.BehaviorResponse.model_validate(b, from_attributes=True) for b in behavior],
    }
)

# Ingestion API



class IngestBehaviorRequest(BaseModel):
    pet_id: int
    text: str

@app.post("/ingest-behavior")
def ingest_behavior(req: IngestBehaviorRequest, db: Session = Depends(get_db)):
    behavior_record = models.Behavior(
        pet_id=req.pet_id,
        score=0,
        description=req.text
    )

    db.add(behavior_record)
    db.commit()
    db.refresh(behavior_record)

    process_ingestion.delay(behavior_record.id, req.text, req.pet_id)

    return {"message": "Behavior ingestion queued", "behavior_id": behavior_record.id}
