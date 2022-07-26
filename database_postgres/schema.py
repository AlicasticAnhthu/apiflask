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
    node_exporter_id = Column(Integer(), ForeignKey('node_exporters.id'), nullable=False)
    token_status = Column(Integer(), unique=False, default=False )
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))

class NodeExporter(Base):
    __tablename__ = 'node_exporters'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    enable = Column(Integer(), default=0)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))
    updated_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))

Base.metadata.create_all(engine)