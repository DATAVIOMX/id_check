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


