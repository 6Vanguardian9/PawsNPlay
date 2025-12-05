from pydantic import BaseModel
from datetime import datetime


# ======================================================
#                      PARENT
# ======================================================

class ParentBase(BaseModel):
    name: str
    email: str

class ParentCreate(ParentBase):
    pass

class ParentResponse(ParentBase):
    id: int

    class Config:
        orm_mode = True


# ======================================================
#                      PET
# ======================================================

class PetBase(BaseModel):
    name: str
    breed: str
    age: int

class PetCreate(PetBase):
    parent_id: int

class PetResponse(PetBase):
    id: int
    parent_id: int

    class Config:
        orm_mode = True


# ======================================================
#                    PET EVENTS
# ======================================================

class PetEventBase(BaseModel):
    event_type: str
    timestamp: datetime
    notes: str | None = None

class PetEventCreate(PetEventBase):
    pet_id: int

class PetEventResponse(PetEventBase):
    id: int

    class Config:
        orm_mode = True


# ======================================================
#                    BEHAVIOR
# ======================================================

class BehaviorBase(BaseModel):
    score: int
    description: str

class BehaviorCreate(BehaviorBase):
    pet_id: int

class BehaviorResponse(BehaviorBase):
    id: int

    class Config:
        orm_mode = True


# ======================================================
#                    REMINDER
# ======================================================

class ReminderBase(BaseModel):
    reminder_text: str
    due_time: datetime

class ReminderCreate(ReminderBase):
    pet_id: int

class ReminderResponse(ReminderBase):
    id: int

    class Config:
        orm_mode = True


class PetFullResponse(PetResponse):
    events: list[PetEventResponse] = []
    behavior: list[BehaviorResponse] = []
    reminders: list[ReminderResponse] = []

    class Config:
        orm_mode = True
