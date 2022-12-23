from db.models.user import User


def create_user(session):
    user = User(email="max", password="max")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
