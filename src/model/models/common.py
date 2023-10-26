from sqlalchemy.orm import DeclarativeBase


# declarative base class
class Base(DeclarativeBase):
    pass


class OperationFailed(Exception):
    pass
