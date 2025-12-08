from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from dbstruct.database_conn import Base


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    # One parent can have many pets
    pets = relationship("Pet", back_populates="parent")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    breed = Column(String)
    age = Column(Integer)

    parent_id = Column(Integer, ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="pets")
    events = relationship("PetEvent", back_populates="pet")
    behavior = relationship("Behavior", back_populates="pet")
    reminders = relationship("Reminder", back_populates="pet")


class PetEvent(Base):
    __tablename__ = "pet_events"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    event_type = Column(String, index=True)
    timestamp = Column(DateTime)
    notes = Column(Text)

    pet = relationship("Pet", back_populates="events")


class Behavior(Base):
    __tablename__ = "behavior"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    score = Column(Integer)
    description = Column(Text)

    pet = relationship("Pet", back_populates="behavior")


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    reminder_text = Column(String)
    due_time = Column(DateTime)

    pet = relationship("Pet", back_populates="reminders")
