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
"""
from bs4 import BeautifulSoup
import requests
# import string
# import re
# import os
# import cv2
# import pytesseract
# import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

def find_qr(img):
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
    extracted_response = BeautifulSoup(response.content, 'html.parser')
    valid_yn = extracted_response.find(name='div', id="menje")
    return [extracted_response, valid_yn]

def query_text(text_dict):
    """
    Function to query the INE page with a text dictionary it breaks the
    captcha using Anticaptcha
    INPUT: dictionary of fields as strings
    OUTPUT: response as list [html, validyn(string)]
    """
    
    return [extracted_response, validyn]

def check_images(front, back):
    """
    Function that checks if an INE provided as two images (front and back)
    is valid through the ine website
    INPUT: front, back : Image as numpy array
    OUTPUT: string representation of HTML response from server
    """
    response = None
    # First we check the OCR as it is easier
    url_qr_front = find_qr(front)
    url_qr_back = find_qr(back)
    if url_qr_front:
        response = query_qr(url_qr_front)
        return response
    if url_qr_back:
        response = query_qr(url_qr_back)
        return response
    # OCR
    proc_front = preprocess_image(front)
    proc_back = preprocess_image(back)
    raw_text_front = extract_text(proc_front)
    raw_text_back = extract_text(proc_back)
    # join text
    full_text = raw_text_front + raw_text_back
    # process text
    processed_text = text_processing(full_text)
    response = query_text(processed_text)
    return response
