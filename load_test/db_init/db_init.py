from sqlalchemy import create_engine, Column, Integer, String, DateTime, SmallInteger, MetaData, ForeignKey
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
engine = create_engine(os.getenv("DATABASE_URL"), echo=True, future=True)
from sqlalchemy.orm import relationship, Session
Base = declarative_base()

class User_Info(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(250), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    schema = "autotest"
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, role={self.role!r})"

class Tests_Registration(Base):
    __tablename__ = "tests_registration"
    id = Column(Integer, primary_key=True, nullable=False)
    start_timestamp = Column(DateTime(timezone=True), nullable=False)
    end_timestamp = Column(DateTime(timezone=True), nullable=False)
    status = Column(SmallInteger, nullable=False)
    author = Column(String(250), unique=False, nullable=False)
    schema = "autotest"
    def __repr__(self):
      return f"Test(id={self.id!r}, start_timestamp={self.start_timestamp!r}, end_timestamp={self.end_timestamp!r}, status={self.status!r})"

class Group(Base):
   __tablename__ = 'groups'

   id = Column(Integer, primary_key = True)
   name = Column(String)
   type = Column(String)

class Test(Base):
   __tablename__ = 'tests'
   
   id = Column(Integer, primary_key = True)
   groupid = Column(Integer, ForeignKey('groups.id'))
   test_name = Column(String)
   link_test_api = Column(String)
   status = Column(String)
   message = Column(String)
   username = Column(String)
   description = Column(String)
   groups = relationship("Group", back_populates = "tests")
   sessionid = Column(String)

Group.tests = relationship("Test", order_by = Test.id, back_populates = "groups")
# Base.metadata.create_all(engine)





