from functools import singledispatch
from typing import Type

from fastapi import HTTPException
from sqlmodel import select, SQLModel, Session


class CRUD:

    @staticmethod
    def create_all(model: Type[SQLModel], session: Session, models_data: [SQLModel]) -> ["model"]:
        models_instance = []
        for data in models_data:
            model_instance = CRUD.create(model, session, data, commit=False)
            models_instance.append(model_instance)
        session.commit()
        for model_instance in models_instance:
            session.refresh(model_instance)
        return models_instance

    @staticmethod
    def create(model: Type[SQLModel], session: Session, model_data: SQLModel, commit=True) -> "model":
        model = model.from_orm(model_data)
        session.add(model)
        if commit:
            session.commit()
            session.refresh(model)
        return model

    @staticmethod
    @singledispatch
    def get_all(model: Type[SQLModel], session: Session) -> ["model"]:
        model_stmt = select(model)
        models = session.exec(model_stmt).all()
        return models

    @staticmethod
    def get_id(model: Type[SQLModel], session: Session, id: int) -> "model":
        model = session.get(model, id)
        return model

    @staticmethod
    def get_page(model: Type[SQLModel], session: Session, count: int = 100, skip: int = 0) -> list["model"]:
        model = session.query(model).limit(count).offset(skip).all()
        return model

    @staticmethod
    @singledispatch
    def patch(model: Type[SQLModel], session: Session, id: int, model_data: SQLModel):
        db_model = CRUD.get_id(model, session, id)
        if not db_model:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = model_data.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_model, key, value)
        session.add(db_model)
        session.commit()
        session.refresh(db_model)
        return db_model

    @staticmethod
    @singledispatch
    def delete(model: Type[SQLModel], session: Session, id: int):
        model = CRUD.get_id(model, session, id)
        session.delete(model)
        session.commit()
        return model
