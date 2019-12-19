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

class AddImageAPI(Resource):
    """
    AddImageAPI is a resource for uploading images to the database where they
    are stored as blobs, the POST request must use either HTTP or multipart
    this class along with image class are needed because JSON can't be used to
    upload a file and sending HTTP requests with files inside is not RESTful.
    """
    def post(self):
        """
        post method to upload an image file, it must specify the filename, file
        and if it is the front or back of the ID
        """
        # Post image to database as HTTP message
        return_dict{"filename": filename, "image-id": image_id, "type": atype
                    "size":size} 
        return return_dict, 201

class ImageAPI(Resource):
    """
    ImageAPI class is a resource for checking and deleting images already
    uploaded, it checks the database for the image_id and either returns the
    file properties or deletes the file
    """
    def get(self, image_id):
        """
        Helper method to check if image exists and its properties
        """
        return {"filename": filename, "image-id":image_id, "size":size,
                "type":atype}, 200

    def delete(self, image_id):
        """
        Helper method to delete image by image_id 
        """
        #Delete image with image id
        return {"image_id": image_id, "message": "succesfuly deleted"}, 200

api.add_resource(AddUserAPI, '/api/v1/users') 
api.add_resource(UsersAPI, '/api/v1/users/<string:userid>')
api.add_resource(AddImageAPI, '/api/v1/images')
api.add_resource(ImageAPI, '/api/v1/images/<string:image_id')

if __name__ == '__main__':
    app.run(debug=True)
