import datetime
import pytz
TIMEZONE = 'Asia/Bangkok'

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
engine = create_engine('postgresql://postgres:o48wktKBegNqQ7rI@172.16.18.47:5432/thu_py')
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

#create 2 databases
class TokenManager(Base):
    __tablename__ = 'token_managers'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    token = Column(String(100), nullable=False)
    local_path = Column(String(100), nullable=False)
    exporter_id = Column(Integer(), ForeignKey('exporters.id'), nullable=False)
    token_status = Column(Integer(), unique=False, default=False )
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))

class ExporterManager(Base):
    __tablename__ = 'exporters'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    secret = Column(String(100), nullable=False)
    target_url = Column(String(100), nullable=False)
    enable = Column(Integer(), default=0)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))
    updated_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))

Base.metadata.create_all(engine)