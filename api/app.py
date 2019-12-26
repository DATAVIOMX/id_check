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

class IDCheck(Resource):
    """
    IDCheck is a class that receives images as numpy arrays, and an API key,
    validates the key and uses OCR to extract the data from the image and query
    INE's database
    """
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("front", type=list, required=True)
        parser.add_argument("back", type=list, required=True)
        parser.add_argument("api_key", type=str, required=True)
        args = parser.parse_args()
        
        # query api_key
        q_str = """SELECT * from users WHERE api_key=?"""
        cur.execute(q_str, (args["api_key"],))
        db_response = cur.fetchone()
        
        # Stuff to log from the call
        userid = 
        call_dt = datetime.datetime.now()
        
        if not db_response:
            # log call
            cur.execute("""INSERT INTO api_calls ()""")
            conn.commit()
            conn.close()
            # return
            return {"error": "key does not exist"}, 403
        else:
            userid
            creation_date
        if status == 1:
            # log call
            cur.execute("""INSERT INTO api_calls""")
            conn.commit()
            conn.close()
            # return
            return {"error": "key does not exist"}, 401
        if status == 2:
            # log call
            cur.execute("""INSERT INTO api_calls""")
            conn.commit()
            conn.close()
            # return
            return {"error": "key does not exist"}, 402
        if api_key_exp_date < today:
            # log call
            cur.execute("""INSERT INTO api_calls""")
            conn.commit()
            conn.close()
            # return
            return {"error": "key is expired"}, 403
        if calls_remaining <= 0:
            # log call
            cur.execute("""INSERT INTO api_calls""")
            conn.commit()
            conn.close()
            # return
            return {"error": "No remaining calls"}, 403
        if calls_remaining > 0 and api_key_exp_date > today and status == 0 and db_response[] == args.api_key:
            results_page = id_check(args["front"], args["back"])
            # log call
            cur.execute("""INSERT INTO api_calls""")
            conn.commit()
            conn.close()
            return {result_page:, call_date, remaining_calls, termination_date}, 200
        return {"error": "Passthrough API"}, 500


api.add_resource(UsersAPI, '/api/v1/users/<int:userid>')
api.add_resource(AddUserAPI, '/api/v1/users') 
#api.add_resource(IDCheck, '/api/v1/id-check')

if __name__ == '__main__':
    app.run(debug=True)
