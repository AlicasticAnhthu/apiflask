from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

#create instance of flask
app = Flask(__name__)
#create API object
api = Api(app)
#create database object
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#sqlarchemy mapper
db = SQLAlchemy(app)

#add a class
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} - {self.salary}"




