#!/usr/bin/env python3
"""
Author: Otto Hahn Herrera
Date: 2019-12-16
Purpose:
RESTful API for id_check
URL has the following format <address>/api/v1/<endpoint>
Where <address> is the server IP or domain and <endpoint can be any of the
following:
users
images
check-ids
"""
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sqlite3


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

class UsersAPI(Resource):
    """
    Users class methods define the calls available through the API to act over
    users in the DB, in this case GET, PUT, POST, DELETE
    """
    def get(self, userid):
        """
        GET method stub, this will query the database for the userid
        """
        date_created = '2019-12-16'
        date_termination = '2020-01-16'
        date_last_payment = '2019-12-16'
        remaining_calls = 1000
        if userid == "AAA111":
            return_dict = {"date-created": date_created,
                       "end-of-service-date": date_termination,
                       "date-of-last-payment": date_last_payment,
                       "remaining-calls": remaining_calls
                        }
            return return_dict
        else:
            return {'error':'user not found'}, 404

class AddUserAPI(Resource):
    def post(self):
        """
        Creates a new user, requires username, and password to generate an API
        key that is returned to the user
        """
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        data = parser.parse_args()         
        api_key = 'SDDFSF123rs12085654'
        return {'username': data['username'], 'password': data["password"],
                "api_key": api_key}, 201

api.add_resource(AddUserAPI, '/api/v1/users') 
api.add_resource(UsersAPI, '/api/v1/users/<string:userid>')

if __name__ == '__main__':
    app.run(debug=True)
