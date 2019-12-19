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
from flask_restful import Resource, Api
import sqlite3


app = Flask(__name__)
api = Api(app)

class Users(Resource):
    """
    Users class methods define the calls available through the API to act over
    users in the DB, in this case GET, PUT, POST, DELETE
    """
    def get(self, userid):
        """
        GET method stub, this will query the database for the userid
        """
        print(userid)
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

api.add_resource(Users, '/api/v1/users/<string:userid>')

if __name__ == '__main__':
    app.run(debug=True)
