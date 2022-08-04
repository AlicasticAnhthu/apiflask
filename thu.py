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
import json

from database_postgres.config import get_db
from crontab import crontab

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
        crontab()

    def insert_token(self, local_path: str, token: str, exporter_id: int):
        # token, local_path, exporter_id = CoreManager().render_link(token, local_path, exporter_id[0])
        # same as in generate function
        print(token)
        insert_query = """INSERT INTO token_managers (token, local_path, exporter_id, token_status) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_query, (token, local_path, str(exporter_id), 0))
        connection.commit()

    def check_token_expired(self, token: str):
        select_exporter_id = """SELECT exporter_id from token_managers"""
        cursor.execute(select_exporter_id)
        exporter_id = cursor.fetchone()
        
        select_secret_query = """SELECT secret from token_managers WHERE exporter_id = %s""" 
        cursor.execute(select_secret_query, (exporter_id))
        secret = cursor.fetchone() # the same secret as in generate function
        token = hmac.new(secret.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

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
        app.route('/template')
        return render_template('haproxy_exporter.sh')


class CoreManager:

    def render_link(self):
        select_exporter_id = """SELECT id from exporters"""
        cursor.execute(select_exporter_id)
        exporter_id = cursor.fetchone()
        print(exporter_id[0])

        select_secret_query = """SELECT secret from exporters WHERE id = %s""" 
        cursor.execute(select_secret_query, (str(exporter_id[0])))
        secret = cursor.fetchone() 
        print(secret)# select accordingly with exporter_id
        token = hmac.new(secret[0].encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        ### get_file?id=exporter_id&token=token
        return exporter_id[0], token, "get_file?file=%(filename)s&id=%(exporter_id)s&token=%(token)s" % {
            "filename": "thu.db",
            "exporter_id": exporter_id[0],
            "token": token
        }

#For GET request list of exporter
class ExporterList(Resource):
    def get(self):
        select_exporter = """SELECT id, name , secret , target_url , enable, created_date from exporters"""
        cursor.execute(select_exporter)
        all_exporters = cursor.fetchall()
        json_exporters = json.dumps(all_exporters, default = list)
        exporters = json.loads(json_exporters)
        # exporters_list = []
        # for exporter in exporters:
        #     exporter_detail= {
        #     "id": exporter.id, 
        #     "name": exporter.name, 
        #     "secret": exporter.secret,
        #     "target_url": exporter.target_url,
        #     "enable": exporter.enable,
        #     }
        #     exporters_list.append(exporter_detail)
        #     print(exporters_list)
        return {"Employees":exporters},200

class Exporter_ID(Resource):
    def get(self, exporter_id):
        select_exporter = """SELECT id, name , secret , target_url , enable, created_date from exporters WHERE id = %s"""
        cursor.execute(select_exporter, (exporter_id))
        exporter = cursor.fetchone()
        json_exporter = json.dumps(exporter, default = list)
        exporter = json.loads(json_exporter)
        return {"Employee":exporter},200

api.add_resource(ExporterList, '/')
api.add_resource(Exporter_ID, '/Detail/<int:exporter_id>')

if __name__ == '__main__':
    # exporter_id, token, local_path = CoreManager().render_link()
    # TokenManager().insert_token(local_path, token, exporter_id)
    app.run(debug=True, port=5002)



    #Resources:
    #https://bobbyhadz.com/blog/python-typeerror-key-expected-bytes-or-bytearray-but-got-str
    #https://newbedev.com/how-to-provide-temporary-download-url-in-flask
    #https://pynative.com/python-mysql-database-connection/