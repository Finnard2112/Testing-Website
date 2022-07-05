from sqlalchemy import Column, Integer, String, DateTime, SmallInteger, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os
engine = create_engine(os.getenv("DATABASE_URL"), echo=True, future=True)

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
    start_timestamp = Column(DateTime(timezone=False), nullable=False)
    end_timestamp = Column(DateTime(timezone=False), nullable=False)
    status = Column(SmallInteger, nullable=False)
    author = Column(String(250), unique=False, nullable=False)
    schema = "autotest"
    def __repr__(self):
        return f"Test(id={self.id!r}, start_timestamp={self.start_timestamp!r}, end_timestamp={self.end_timestamp!r}, status={self.status!r})"

# Base.metadata.schema = "autotest"
# Base.metadata.create_all(engine)
