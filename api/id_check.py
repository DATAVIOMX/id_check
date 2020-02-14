#!/usr/bin/env python3
"""
check_id is a module that holds functions to check an INE id either from the
image or the data fields
functions are better for this as shown in:
https://codereview.stackexchange.com/questions/201672/
                               image-processing-using-python-oop-library
See link of the talk referenced on the answer
Also, as everything is related (even the calls) we can split everything
into functions, without loss of functionality and without too many imports

Contents

1. check_id_text() OK
2. check_id_img() OK
3. get_qr() OK
4. query_qr() OK
5. clean_qr_response OK
6. prep_img()
7. ocr_img() OK
8. proc_ocr_text()
9. query_web()
10. proc_web_response() WIP

"""
from bs4 import BeautifulSoup
import requests
# import string
# import re
# import os
# import cv2
import pytesseract
# import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask


API_KEY = ""

def get_qr(img):
    """
    Simple function that decodes a QR code from an image returns the URL
    inside the code or None (on failure)
    INPUT: image as cv2 image
    OUTPUT: url as string or None
    """
    qr_data = None
    url = decode(img, symbols=[ZBarSymbol.QRCODE])
    if url:
        return url
    return qr_data

def query_qr(url):
    """
    Simple method to query if a QR code from an INE is valid
    INPUT: url as string
    OUTPUT: response as list [html, valid]
    """
    response = requests.get(url)
    return response.content

def clean_qr_response(resp):
    """
    Cleanup function to extract the boolean value of valid ID from the
    HTML content of the response
    """
    extracted_response = BeautifulSoup(resp, 'html.parser')
    valid_yn = extracted_response.find(name='div', id="menje")
    return {"response": extracted_response, "valid": valid_yn}

def prep_img(img):
    """
    Image processing steps, this function receives an image and does the
    following:
    - binarization
    - Denoising
    - Filtering
    - Edge detection
    - Perspective warping
    It receives an image and returns the processed image
    """
    proc_img = None
    return proc_img

def ocr_img(img):
    """
    Calls tesseract on a processed image
    receives an image and returns a string
    """
    try:
        text = pytesseract.image_to_string(img, lang="spa")
    except ValueError:
        text = None
    return text

def proc_ocr_text(text):
    """
    Receives a string and returns a dictionary containing the ID fields
    and the ID type
    """
    id_dict = {}
    return id_dict

def query_web(id_dict, key):
    """
    Simple web caller that receives a dictionary of data, fills a form
    and calls the INE website, returns the HTML response
    """
    resp = None
    return resp.content

def proc_web_response(content):
    """
    Receives a raw HTML response from INE and extracts if the ID is valid
    as a Boolean value, returns its input and the extracted value as a
    dictionary
    """
    resp_dict = {"Error":"Please provide better images"}
    if content is not None:
        extracted_response = content
        # valid_yn =  TO DO
        return {"response": extracted_response, "valid": valid_yn}
    return resp_dict

def check_id_text(text_dict, key):
    """
    Function to query the INE page with a text dictionary it breaks the
    captcha using Anticaptcha
    INPUT: dictionary of fields as strings
    OUTPUT: response as list [html, validyn(string)]
    """
    return_dict = {"Error": "Problem calling INE"}
    response = query_web(text_dict, key)
    if response:
        return_dict = proc_web_response(response)
    return return_dict

def check_id_img(front, back):
    """
    Function that checks if an INE provided as two images (front and back)
    is valid through the ine website
    INPUT: front, back : Image as numpy array
    OUTPUT: string representation of HTML response from server
    """
    response = None
    return_dict = {}
    # First we check the OCR as it is easier
    url_qr_front = get_qr(front)
    url_qr_back = get_qr(back)
    if url_qr_front:
        response = query_qr(url_qr_front)
        return_dict = clean_qr_response(response)
        return return_dict
    if url_qr_back:
        response = query_qr(url_qr_back)
        return_dict = clean_qr_response(response)
        return return_dict
    # OCR
    proc_front = prep_img(front)
    proc_back = prep_img(back)
    raw_text_front = ocr_img(proc_front)
    raw_text_back = ocr_img(proc_back)
    # join text
    full_text = raw_text_front + raw_text_back
    # process text
    processed_text = proc_ocr_text(full_text)
    # query INE website
    return_dict = check_id_text(processed_text, API_KEY)
    return return_dict
