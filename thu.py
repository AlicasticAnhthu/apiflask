import hashlib
import hmac
import time
import datetime
import pytz
from cgitb import enable
from pickle import TRUE
import resource
from unicodedata import name
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from jinja2 import Environment, PackageLoader, select_autoescape
# from sqlalchemy import ForeignKey
# env = Environment(
#     loader=PackageLoader("yourapp"),
#     autoescape=select_autoescape()
# )
TIMEZONE = 'Asia/Bangkok'

#create instance of flask
app = Flask(__name__)
#create API object
api = Api(app)

DATA = {
    'users': [
        
    ]
}

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
    updated_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))

class NodeExporter(Base):
    __tablename__ = 'node_exporters'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    enable = Column(Integer(), default=0)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))
    updated_date = Column(DateTime(timezone=True), default=datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))

Base.metadata.create_all(engine)

# class ExporterManager:

#     def list_exporter(self):
        
#         pass

connection = psycopg2.connect(user="postgres",
                                  password="o48wktKBegNqQ7rI",
                                  host="172.16.18.47",
                                  port="5432",
                                  database="thu_py")
cursor = connection.cursor()

class TokenManager:

    @staticmethod
    def remove_all_previous_token(exporter_id: int) -> bool:
        secret = "thu_pyhohohihihihehe"  # same as in generate function
        time_limit = 5 * 60  # maximum time in sec that you want them to start download after the link has been generated.
        
        #fetch update_date from database
        update_date_select_query = """SELECT LAST updated_date from token_managers WHERE 1"""
        cursor.execute(update_date_select_query)
        updated_date = cursor.fetchall()

        #fetch create_date from database
        created_date_select_query = """SELECT LAST created_date from token_managers WHERE 1"""
        cursor.execute(created_date_select_query)
        created_date = cursor.fetchall()

        #fetch token from database
        token_select_query = """SELECT LAST token from token_managers WHERE 1"""
        cursor.execute(token_select_query)
        token = cursor.fetchall()

        if (time.time() - int(updated_date - created_date)) > time_limit:  #timeout, return False
            return False
        if hmac.new(secret, str(updated_date - created_date), hashlib.sha256).hexdigest() == token:  # Check the token is available or not
            return True
        else:
            return False

if __name__ == '__main__':
    app.run(debug=True, port=5001)

#     def insert_token(self, local_path: str, token: str):
#         pass

#     def check_token_expired(self, token: str):
#         pass


# class DatasourceManager:

#     def get_datasource(self, datasource_id: int):
#         pass


# class TemplateManager:

#     def render(self):
#         pass


# class CoreManager:

#     def render_link(self):
#         pass
