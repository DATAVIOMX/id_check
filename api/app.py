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
import werkzeug
import secrets
import datetime
from dateutil.relativedelta import *

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
        conn = sqlite3.connect("id-check-db.sqlite")
        cur = conn.cursor()
        q_str = """SELECT creation_date, api_key_exp_date, calls_remaining
                from users where userid=?"""
        cur.execute(q_str, (userid,))
        result = cur.fetchone()
        conn.close()
        print(result)
        if not result:
            return {'error':'user not found'}, 404
        else:
            return_dict = {"date-created": result[0],
                       "api-key-expiration-date": result[1],
                       "remaining-calls": result[2]
                        }
            return return_dict, 200


class AddUserAPI(Resource):
     def post(self):
        """
        Creates a new user, requires username, and password to generate an API
        key that is returned to the user
        """
        # Get last user id from DB
        conn = sqlite3.connect("id-check-db.sqlite")
        cur = conn.cursor()
        q_str = """SELECT MAX(userid) from users"""
        cur.execute(q_str)
        userid = cur.fetchone()[0] + 1
        api_key = secrets.token_urlsafe(40)[1:32]
        now = datetime.datetime.now()
        creation_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        update_date = creation_date
        api_key_exp_date_obj = now + relativedelta(months=+1)
        api_key_exp_date = api_key_exp_date_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
        status = 2
        calls_remaining = 1000
        
        # Load in DB
        cur.execute("""INSERT INTO users (userid, creation_date, update_date,
                    status, api_key, api_key_exp_date, calls_remaining) 
                    VALUES (?,?,?,?,?,?,?)""",(userid, creation_date, 
                    update_date, status, api_key, api_key_exp_date,
                    calls_remaining))
        conn.commit()
        conn.close()
        return {"userid": userid, "creation_date": creation_date, 
                "update_date": update_date, "status": "inactive", 
                "api_key": api_key, "api_key_exp_date": api_key_exp_date,
                "calls_remaining": calls_remaining }, 201

# class IDCheck(Resource):
    # """
    # IDCheck is a class that receives images as numpy arrays, and an API key,
    # validates the key and uses OCR to extract the data from the image and query
    # INE's database
    # """
    # def post(self):
        # parser.add_argument("front")
        # parser.add_argument("back")
        # parser.add_argument("api_key")
        # # query api_key
        # # If key does not exist
            # return {error: key does not exist}, 404
        # # if key is invalid (
            # return {error: Expired key, contact your provider, cause:}, 503
        # # if key is valid, payment is OK and has remaining calls
        # result_page = id_check.check(front, back)
        # return {result_page:, call_date, remaining_calls, termination_date}, 200

api.add_resource(UsersAPI, '/api/v1/users/<int:userid>')
api.add_resource(AddUserAPI, '/api/v1/users') 
#api.add_resource(IDCheck, '/api/v1/id-check')

if __name__ == '__main__':
    app.run(debug=True)