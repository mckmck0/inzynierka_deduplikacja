from typing import TYPE_CHECKING
import database as _database
import models as _models
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    _database.Base.metadata.create_all(bind=_database.engine)
    print("Tables created successfully")


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_contact(contact: _schemas.CreateContact,
                         db: "Session") -> _schemas.Contact:
    contact = _models.Contact(**contact.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return _schemas.Contact.from_orm(contact)


async def get_contacts(db: "Session") -> list[_schemas.Contact]:
    contacts = db.query(_models.Contact).all()
    return list(map(_schemas.Contact.from_orm, contacts))


async def get_contact(contact_id: int, db: "Session"):
    contact = db.query(_models.Contact).filter(_models.Contact.id == contact_id).first()
    return contact


async def delete_contact(contact: _models.Contact, db: "Session"):
    db.delete(contact)
    db.commit()


async def update_contact(contact: _models.Contact,
                         contact_data: _schemas.CreateContact,
                         db: "Session") -> _schemas.Contact:
    for field, value in contact_data:
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)

    return _schemas.Contact.from_orm(contact)
