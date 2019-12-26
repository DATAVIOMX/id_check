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
import json

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
        req_data = request.get_json()
        raw_req = json.dumps(req_data)
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("front", type=list, required=True)
        parser.add_argument("back", type=list, required=True)
        parser.add_argument("api_key", type=str, required=True)
        args = parser.parse_args()
        # print(args)
        
        conn = sqlite3.connect("id-check-db.sqlite")
        cur = conn.cursor()
        
        today = datetime.datetime.now()
        
        # query api_key
        q_str = """SELECT userid,
                    api_key, 
                    api_key_exp_date,
                    status, 
                    calls_remaining
                    from users WHERE api_key=?"""
        cur.execute(q_str, (args["api_key"],))
        db_response = cur.fetchone()
        print("DB response", db_response)
        
        if not db_response:
            # log call
            call_dt = datetime.datetime.now()
            cur.execute("""INSERT INTO api_calls (call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (?,?,?,?,?)""", (call_dt, 'id-check', 403, raw_req,
                        '{"error":"key does not exist"}',))
            conn.commit()
            conn.close()
            return {"error": "key does not exist"}, 403
        else:
            # Stuff to log from the call
            userid = db_response[0]
            api_key = db_response[1]
            api_exp = datetime.datetime.strptime(db_response[2], "%Y-%m-%dT%H:%M:%S.%f")
            status = db_response[3]
            calls = db_response[4]
            call_dt = datetime.datetime.now()
            if status == 1:
                # log call
                cur.execute("""INSERT INTO api_calls (userid, api_key, call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (?,?,?,?,?,?,?)""", (userid, api_key, call_dt, 'id-check', 403, raw_req,
                        '{"error":"payment processing in progress"}',))
                conn.commit()
                conn.close()
                return {"error": "payment processing in progress"}, 401
            elif status == 2:
                # log call
                cur.execute("""INSERT INTO api_calls (userid, api_key, call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (?,?,?,?,?,?,?)""", (userid, api_key, call_dt, 'id-check', 403, raw_req,
                        '{"error":"payment required"}',))
                conn.commit()
                conn.close()
                return {"error": "payment required"}, 402
            elif api_exp < today:  # <-- date comparison required
                print("expired key")
                # log call
                cur.execute("""INSERT INTO api_calls (userid, api_key, call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (?,?,?,?,?,?,?)""", (userid, api_key, call_dt, 'id-check', 403, raw_req,
                        '{"error":"key is expired"}',))
                conn.commit()
                conn.close()
                return {"error": "key is expired"}, 403
            elif calls <= 0:
                # log call
                cur.execute("""INSERT INTO api_calls (userid, api_key, call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (?,?,?,?,?,?,?)""", (userid, api_key, call_dt, 'id-check', 403, raw_req,
                        '{"error":"No remaining calls"}',))
                conn.commit()
                conn.close()
                return {"error": "No remaining calls"}, 403
            else:
                # NOTE: results_page needs to be in a try except or in an if
                # block to return either a 200 status or a 500 status
                # results_page = id_check(args["front"], args["back"])
                # log call
                cur.execute("""INSERT INTO api_calls (userid, api_key, call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (?,?,?,?,?,?,?)""", (userid, api_key, call_dt, 'id-check', 403, raw_req,
                        '{"success":"call successful"}',))
                conn.commit()
                conn.close()
                return {"success":"call successful"}, 200


api.add_resource(UsersAPI, '/api/v1/users/<int:userid>')
api.add_resource(AddUserAPI, '/api/v1/users') 
api.add_resource(IDCheck, '/api/v1/id-check')

if __name__ == '__main__':
    app.run(debug=True)
