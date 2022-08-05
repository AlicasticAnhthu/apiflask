import datetime
import pytz
import psycopg2
from jinja2 import Environment, PackageLoader, select_autoescape
from config import get_db
connection, cur = get_db()

TIMEZONE = 'Asia/Bangkok'

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table, sql, text, TIMESTAMP
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
    created_date = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(TIMESTAMP(timezone=True), server_default =sql.func.now(),onupdate=sql.func.current_timestamp())

class ExporterManager(Base):
    __tablename__ = 'exporters'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    secret = Column(String(100), nullable=False)
    target_url = Column(String(100), nullable=False)
    enable = Column(Integer(), default=0)
    created_date = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.secret} - {self.target_url} - {self.enable} - {self.created_date}"

Base.metadata.create_all(engine)

def insert_exportermanager_list(exporter_list):
    """ insert multiple exporter into the exporters table  """
    sql = "INSERT INTO exporters(name , secret , target_url , enable ) VALUES(%s, %s, %s, %s)"
    try:
        # execute the INSERT statement
        cur.executemany(sql, exporter_list)
        # commit the changes to the database
        connection.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
def insert_tokenmanager_list(token_list):
    """ insert multiple token into the token_managers table  """
    sql = "INSERT INTO token_managers (name , secret , target_url , enable , created_date , updated_date) VALUES(%s, %s, %s, %s, %s, %s)"
    try:
        # execute the INSERT statement
        cur.executemany(sql, token_list)
        # commit the changes to the database
        connection.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    

if __name__ == '__main__':
    # insert multiple vendors
    insert_exportermanager_list([
        ('HA_proxy exporter', 'HA_proxy exporter123@', 'http://localhost:5000/api/v1/exporter/1', 1),
    ])