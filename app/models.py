from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base

from enum import Enum as PythonEnum

Base = declarative_base()


class MD5Status(PythonEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class MD5Result(Base):
    __tablename__ = "md5_results"

    id = Column(Integer, primary_key=True, index=True)
    promise_id = Column(String, unique=True)
    md5_hash = Column(String)
    status = Column(Enum(MD5Status), default=MD5Status.PENDING, nullable=False)
