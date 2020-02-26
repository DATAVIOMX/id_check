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
import datetime
import json
import secrets
from dateutil.relativedelta import relativedelta
import psycopg2 as db
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import id_check

app = Flask(__name__)
api = Api(app)


class UsersAPI(Resource):
    """
    Users class methods define the calls available through the API to act over
    users in the DB, in this case GET, PUT, POST, DELETE
    """
    def get(self, userid):
        """
        GET method, this will query the database for the userid
        """
        print("USERID", userid, type(userid))
        conn = db.connect("dbname='id_check_db' user='otto' host='localhost' password=ottoman")
        cur = conn.cursor()
        q_str = """SELECT creation_date, api_key_exp_date, calls_remaining
                from users where userid=%s"""
        cur.execute(q_str, (userid,))
        result = cur.fetchone()
        conn.close()
        print(result)
        if not result:
            return {'error':'user not found'}, 404
        return_dict = {"date-created": result[0].strftime("%Y-%m-%dT%H:%M:%S.%f"),
                       "api-key-expiration-date": result[1].strftime("%Y-%m-%dT%H:%M:%S.%f"),
                       "calls-made": result[2]}
        return return_dict, 200


class AddUserAPI(Resource):
    """
    Resource subclass to generate an endpoint for adding users to the
    database the class contains only a post method.
    """
    def post(self):
        """
        Creates a new user, to generate an API
        key that is returned to the user
        """
        # Get last user id from DB
        conn = db.connect("dbname='id_check_db' user='otto' host='localhost' password=ottoman")
        cur = conn.cursor()
        api_key = secrets.token_urlsafe(40)[1:32]
        now = datetime.datetime.now()
        creation_date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        update_date = creation_date
        api_key_exp_date_obj = now + relativedelta(months=+1)
        api_key_exp_date = api_key_exp_date_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
        status = 2
        calls_remaining = 0
        # Load in DB
        cur.execute("""INSERT INTO users (userid, creation_date, update_date,
                    status, api_key, api_key_exp_date, calls_remaining)
                    VALUES (gen_random_uuid(),%s,%s,%s,%s,%s,%s)""",
                    (now, now, status, api_key, api_key_exp_date,
                     calls_remaining))
        conn.commit()
        conn.close()
        return {"creation-date": creation_date,
                "update-date": update_date, "status": "inactive",
                "api-key": api_key,
                "calls-made": calls_remaining}, 201

class IDCheck(Resource):
    """
    IDCheck is a class that receives images as numpy arrays, and an API key,
    validates the key and uses OCR to extract the data from the image and query
    INE's database
    """
    def post(self):
        """
        POST method to generate a POST request to the ID check API,
        requres the API key, and front and back images of the ID
        """
        req_data = request.get_json()
        #json.dumps(req_data) = json.dumps(req_data)
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("front", type=list, required=True)
        parser.add_argument("back", type=list, required=True)
        parser.add_argument("api_key", type=str, required=True)
        args = parser.parse_args()

        # connect to database
        conn = db.connect("dbname='id_check_db' user='otto' host='localhost' password=ottoman")
        cur = conn.cursor()

        # query api_key
        q_str = """SELECT userid,
                    status
                    from users WHERE api_key=%s"""
        cur.execute(q_str, (args["api_key"],))
        db_response = cur.fetchone()
        # print("DB response", db_response)

        # API KEY DOES NOT EXISTS
        if not db_response:
            # log call
            # get max callid
            call_dt = datetime.datetime.now()
            cur.execute("""INSERT INTO api_calls (call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (%s,%s,%s,pgp_sym_encrypt(%s,'longsecretencryptionkey'),
                        pgp_sym_encrypt(%s,'longsecretencryptionkey'))""",
                        (call_dt, 'id-check', 404, json.dumps(req_data),
                         '{"error":"key does not exist"}',))
            conn.commit()
            conn.close()
            return {"error": "key does not exist"}, 404
        # Stuff to log from the call
        userid = db_response[0]
        status = db_response[1]
        call_dt = datetime.datetime.now()
        if status == 1:
            # log call
            cur.execute("""INSERT INTO api_calls (userid, call_date,
                        call_point, status_code, call_text, response)
                        VALUES (%s,%s,%s,%s,pgp_sym_encrypt(%s,
                        'longsecretencryptionkey'), 
                        pgp_sym_encrypt(%s,'longsecretencryptionkey'))""",
                        (userid, call_dt, 'id-check', 403, json.dumps(req_data),
                         '{"error":"payment processing in progress"}',))
            conn.commit()
            conn.close()
            return {"error": "payment processing in progress"}, 401
        if status == 2:
            # log call
            cur.execute("""INSERT INTO api_calls (userid, call_date,
                        call_point, status_code, call_text, response)
                        VALUES (%s,%s,%s,%s,pgp_sym_encrypt(%s,
                        'longsecretencryptionkey'),
                        pgp_sym_encrypt(%s,'longsecretencryptionkey'))""",
                        (userid, call_dt, 'id-check', 402, json.dumps(req_data),
                         '{"error":"payment required"}',))
            conn.commit()
            conn.close()
            return {"error": "payment required"}, 402
        # NOTE: results_page needs to be in a try except or in an if
        # block to return either a 200 status or a 500 status
        # We need to convert args["front"] and "back" to ndarray of given shape
        front = np.fromstring(args["front"], dtype=np.uint8)
        back = np.fromstring(args["front"], dtype=np.uint8)
        np.reshape(front, tuple(args["shape_f"]))
        np.reshape(back, tuple(args["shape_b"]))
        results = id_check(front, back)
        # log call
        cur.execute("""INSERT INTO api_calls (userid, call_date,
                    call_point,status_code, call_text, response)
                    VALUES (%s,%s,%s,%s,pgp_sym_encrypt(%s,
                    'longsecretencryptionkey'),
                    pgp_sym_encrypt(%s,'longsecretencryptionkey'))""",
                    (userid, call_dt, 'id-check', 200, json.dumps(req_data),
                     '{"success":"call successful"}',))
        conn.commit()
        conn.close()
        return {"success":"call successful"}, 200

class TextCheck(Resource):
    """
    Text check is a class that only receives the text data and API key
    from the client and validates the key and queries INE's database
    """
    def post(self):
        """
        Function that defines the post method for id_check using text only
        this requires type of ID, elector key, year of issue, ocr horizontal
        ocr vertical, the CIC field, and the citizen's key besides the API
        key
        """
        req_data = request.get_json()
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("tipo_cred", type=str, required=True)
        parser.add_argument("cve_elec", type=str, required=True)
        parser.add_argument("emision", type=str, required=True)
        parser.add_argument("ocr_vertical", type=str, required=True)
        parser.add_argument("ocr_horizontal", type=str, required=True)
        parser.add_argument("cic", type=str, required=True)
        parser.add_argument("cve_ciudadano", type=str, required=True)
        parser.add_argument("api_key", type=str, required=True)
        args = parser.parse_args()
        conn = db.connect("dbname='id_check_db' user='otto' host='localhost' password=ottoman")
        cur = conn.cursor()
        # query api_key
        q_str = """SELECT userid,
                    api_key, 
                    status
                    from users WHERE api_key=%s"""
        cur.execute(q_str, (args["api_key"],))
        db_response = cur.fetchone()
        print("DB response", db_response)
        if not db_response:
            # log call
            # get max callid
            cur.execute("SELECT max(callid) from ap_calls")
            maxid = cur.fetchone()[0] + 1
            call_dt = datetime.datetime.now()
            cur.execute("""INSERT INTO api_calls (callid, call_date, call_point,
                        status_code, call_text, response) VALUES 
                        (%s,%s,%s,%s,pgp_sym_encrypt(%s, 'longsecretencryptionkey'))""",
                        (maxid, call_dt, 'id-check', 404, json.dumps(req_data),
                         '{"error":"key does not exist"}',))
            conn.commit()
            conn.close()
            return {"error": "key does not exist"}, 404

        # Stuff to log from the call
        userid = db_response[0]
        status = db_response[1]
        call_dt = datetime.datetime.now()
        if status == 1:
            # log call
            cur.execute("""INSERT INTO api_calls (userid, call_date, call_point,
                    status_code, call_text, response) VALUES 
                    (%s,%s,%s,%s,pgp_sym_encrypt(%s,'longsecretencryptionkey'),
                    pgp_sym_encrypt(%s,'longsecretencryptionkey'))""",
                        (userid, call_dt, 'id-check', 403, json.dumps(req_data),
                         '{"error":"payment processing in progress"}',))
            conn.commit()
            conn.close()
            return {"error": "payment processing in progress"}, 401
        if status == 2:
            # log call
            cur.execute("""INSERT INTO api_calls (userid, call_date, call_point,
                    status_code, call_text, response) VALUES 
                    (%s,%s,%s,%s,
                    pgp_sym_encrypt(%s,'longsecretencryptionkey'),
                    pgp_sym_encrypt(%s,'longsecretencryptionkey'))""",
                        (userid, call_dt, 'id-check', 402,
                         json.dumps(req_data), '{"error":"payment required"}',))
            conn.commit()
            conn.close()
            return {"error": "payment required"}, 402
        # NOTE: results_page needs to be in a try except or in an if
        # block to return either a 200 status or a 500 status
        text_dict = args
        del text_dict["api_key"]
        results =id_check.check_id_text(args)
        # log call
        cur.execute("""INSERT INTO api_calls (userid, call_date, call_point,
                status_code, call_text, response) VALUES 
                (%s,%s,%s,%s,pgp_sym_encrypt(%s,'longsecretencryptionkey'),
                pgp_sym_encrypt(%s,'longsecretencryptionkey'))""",
                    (userid, call_dt, 'id-check', 200, json.dumps(req_data),
                     '{"resultados":'+results_page+'}',))
        conn.commit()
        conn.close()
        return {"resultados":results_page}, 200





api.add_resource(UsersAPI, '/api/v1/users/<userid>')
api.add_resource(AddUserAPI, '/api/v1/users')
api.add_resource(IDCheck, '/api/v1/id-check/images')
api.add_resource(TextCheck, '/api/v1/id-check/text')

if __name__ == '__main__':
    app.run(debug=True)
