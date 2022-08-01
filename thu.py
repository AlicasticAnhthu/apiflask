import hashlib
import hmac
import time

from cgitb import enable
from pickle import TRUE
import resource
from unicodedata import name
from flask import Flask, request, jsonify, make_response, send_file, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from jinja2 import Environment, PackageLoader, select_autoescape

from database_postgres.config import get_db
from database_postgres.schema import *

# from sqlalchemy import ForeignKey
# env = Environment(
#     loader=PackageLoader("yourapp"),
#     autoescape=select_autoescape()
# )


#create instance of flask
app = Flask(__name__)
#create API object
api = Api(app)

connection, cursor= get_db()

class TokenManager:

    @staticmethod
    def remove_all_previous_token(exporter_id: int) -> bool:
        pass

    def insert_token(self, local_path: str, token: str):
        local_path = CoreManager().render_link()
        secret = "thu_pyhohohihihihehe"  # same as in generate function
        token = hmac.new(secret, digestmod=hashlib.sha256).hexdigest()
        insert_query = """INSERT INTO token_managers (local_path, token) VALUES (%s, %s)"""
        cursor.execute(insert_query, (local_path, token))
        connection.commit()

    def check_token_expired(self, token: str):
        secret = "thu_pyhohohihihihehe"  # same as in generate function
        time_limit = 5 * 60  # maximum time in sec that you want them to start download after the link has been generated.
        
        #fetch update_date from database
        update_date_select_query = """SELECT LAST updated_date from token_managers"""
        cursor.execute(update_date_select_query)
        updated_date = cursor.fetchall()

        #fetch create_date from database
        created_date_select_query = """SELECT LAST created_date from token_managers"""
        cursor.execute(created_date_select_query)
        created_date = cursor.fetchall()

        #fetch token from database
        token_select_query = """SELECT LAST token from token_managers"""
        cursor.execute(token_select_query)
        token = cursor.fetchall()

        if (time.time() - int(updated_date - created_date)) > time_limit:  #timeout, return False
            return False
        if hmac.new(secret, str(updated_date - created_date), hashlib.sha256).hexdigest() == token:  # Check the token is available or not
            return True
        else:
            return False

# class DatasourceManager:

#     def get_datasource(self, datasource_id: int):
#         pass


class TemplateManager:

    def render(self):
        pass


class CoreManager:

    def render_link(self):
        secret = "thu_pyhohohihihihehe"  # such as generate from os.urandom(length)
        current_time = str(int(time.time()))
        token = hmac.new(secret.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        ### get_file?id=exporter_id&token=token

        return "get_file?file=%(filename)s&time=%(current_time)s&token=%(token)s" % {
            "filename": "thu.db",
            "current_time": current_time,
            "token": token
        }

if __name__ == '__main__':
    link = CoreManager().render_link()
    print(link)
    send_file("/thu.db", as_attachment=True) 
    app.run(debug=True, port=5001)