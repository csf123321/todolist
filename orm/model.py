from sqlalchemy import INTEGER, Column, ForeignKey, String,DateTime,Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(INTEGER(), primary_key=True)


class Users(BaseModel):
    __tablename__ = "users"
    username = Column(String(100),unique=True)
    password = Column(String(100))
    email = Column(String(100),unique=True)
    todolist = relationship("ToDoList",back_populates='user')
    session = relationship('Session',uselist=False)


class ToDoList(BaseModel):
    __tablename__ = "todolist"
    name = Column(String(100))
    description = Column(Text(200))
    createDate = Column(DateTime())
    deadline = Column(DateTime())
    state = Column(INTEGER,nullable=False,default=0)
    user_id = Column(INTEGER,ForeignKey('users.id'))
    user = relationship("Users",back_populates="todolist")


class Session(BaseModel):
    __tablename__ = "session"
    user_id = Column(INTEGER,ForeignKey('users.id'))
    session = Column(String(100))
    user = relationship("Users",uselist=False,back_populates='session')