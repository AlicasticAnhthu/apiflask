from pickle import TRUE
import resource
from unicodedata import name
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("yourapp"),
    autoescape=select_autoescape()
)

#create instance of flask
app = Flask(__name__)
#create API object
api = Api(app)

DATA = {
    'users': [
        
    ]
}
#create database object
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thu.db'
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

#For GET request to http://localhost:5000
class getEmployee(Resource):
    def get(self):
        employee=Employee.query.all()
        emp_list = []
        for emp in employee:
            emp_detail = {'id':emp.id,
            'firstname':emp.firstname,
            'lastname':emp.lastname,
            'gender':emp.gender, 
            'salary':emp.salary}
            emp_list.append(emp_detail)
        return {"Employees":emp_list},200

#For POST request to http://localhost:5000/employee
class AddEmployee (Resource):
    def post(self):
        if request.is_json:
            emp = Employee(firstname=request.json['firstname'], 
            lastname=request.json['lastname'],
            gender=request.json['gender'],
            salary=request.json['salary'])
            db.session.add(emp)
            db.session.commit()
            #return json response
            return make_response(jsonify({
                'id':emp.id,
                'firstname':emp.firstname,
                'lastname':emp.lastname,
                'gender':emp.gender, 
                'salary':emp.salary}), 201)
        else:
            return {'Error':'Request must be Json'},400

#For PUT request to http://localhost:5000/update/?
class UpdateEmployee (Resource):
    def put(self,id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'Error':'Employee not found'},404
            else:
                emp.firstname = request.json['firstname']
                emp.lastname = request.json['lastname']
                emp.gender = request.json['gender']
                emp.salary = request.json['salary']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'Error':'Not found'}, 404

#For delete request to http://localhost:5000/delete/?
class DeleteEmployee (Resource):
    def delete(self,id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'Error':'Employee not found'},404
        db.session.delete(emp)
        db.session.commit()
        return f'{id} is deleted', 200

api.add_resource(getEmployee, '/')
api.add_resource(AddEmployee, '/add')
api.add_resource(UpdateEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)


#cai them flask swagger
#restless vs restful
#standardization openapi


