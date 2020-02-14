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
10. proc_web_response() OK (check)

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
    if img:
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

def proc_text(text, id_type):
    """
    Text processing routine, takes the OCR text and does extraction of
    relevant fields based on regexes
    INPUT: text, id_type
    OUTPUT: id_dict a dictionary with different information fields based
    on the ID type
    REVISAR
    """
    id_dict = None
    if id_type == 'a':
        try:
            regex_find = re.compile(r"\w{6}\d{8}\w\d{3}")
            cve_elector_completo = list(filter(regex_find.search, text_vector))[0]
            cve_elector = regex_find.findall(cve_elector_completo)[0]
        except:
            cve_elector = 'NOT DETECTED'
        emision = "placeholder"
        ocr_v = "placeholder"
        cic = ''
        ocr_h = ''
        cve_ciudadano = ''
        err_msg = ''
    if id_type == 'd':
        try:
            regex_find = re.compile(r"\w{6}\d{8}\w\d{3}")
            cve_elector_completo = list(filter(regex_find.search, text_vector))[0]
            cve_elector = regex_find.findall(cve_elector_completo)[0]
        except:
            cve_elector = 'NOT DETECTED'
        emision = ''
        ocr_v = ''
        cve_ciudadano = ''
        err_msg = ''
        flt = np.array(['DMEX' in mystring for mystring in text_vector])
        try:
            cic, ocr_h = np.array(text_vector)[flt][0].split('<<')
            cic = cic[-10:len(cic)]
        except:
            cic, ocr_h = ("NOT DETECTED", "NOT DETECTED")
    if id_type == 'e':
        try:
            regex_find = re.compile(r"\w{6}\d{8}\w\d{3}")
            cve_elector_completo = list(filter(regex_find.search, text_vector))[0]
            cve_elector = regex_find.findall(cve_elector_completo)[0]
        except:
            cve_elector = 'NOT DETECTED'
        emision = ''
        ocr_v = ''
        ocr_h = ''
        err_msg = ''
        # Buscar en todos los resultados
        flt = np.array(['DMEX' in mystring for mystring in text_vector])
        try:
            cic, cve_ciudadano = np.array(text_vector)[flt][0].split('<<')
            cic = cic[-10:len(cic)]
        except:
            cic, cve_ciudadano = ("NOT DETECTED", "NOT DETECTED")
    if id_type == 'NOT DETECTED':
        cve_elector = ''
        emision = ''
        ocr_v = ''
        ocr_h = ''
        cic = ''
        cve_ciudadano = ''
        err_msg = 'ERROR: Por favor mejorar la calidad de la imagen'
    outputs = list()
    outputs.extend([str(id_type), str(cve_elector), str(emision),
                    str(ocr_v), str(ocr_h), str(cic), str(cve_ciudadano),
                    str(err_msg)])
    keys_ = ['tipo_cred', 'cve_elec', 'emision', 'ocr_vertical', \
              'ocr_horizontal', 'cic', 'cve_ciudadano', 'err_msg']

    id_dict = dict(zip(keys_, outputs))

    return id_dict

def get_id_type(text):
    """
    Classifier of IDs based on the text
    INPUT: text
    OUTPT: ID type (as a character), None on failure
    """
    id_type = None
    if ((any('TO FEDERAL' in mystring for mystring in text)) and
            ((any('DMEX' in mystring for mystring in text)) or
             (any('IDMEX' in mystring for mystring in text)) or
             (any('0MEX' in mystring for mystring in text)))):
        id_type = 'd'
    if(any('TO NACIONAL' in mystring for mystring in text) or
       any('TO NACION' in mystring for mystring in text)):
        id_type = 'e'
    if(any('TO FEDERAL' in mystring for mystring in text) and
       ((any('DOCUMENTO' in mystring for mystring in text)) or
        (any('TACHA' in mystring for mystring in text)) or
        (any('ENMENDADURA' in mystring for mystring in text)) or
        (any('INTRANSFERIBLE' in mystring for mystring in text)))):
        id_type = 'a'
    return id_type

def proc_ocr_text(text):
    """
    Receives a string and returns a dictionary containing the ID fields
    and the ID type
    """
    id_dict = None
    id_type = get_id_type(text)
    if id_type:
        id_dict = proc_text(text, id_type)
    return id_dict

def query_web(id_dict):
    """
    Simple web caller that receives a dictionary of data, fills a form
    and calls the INE website, returns the HTML response
    """
    resp = None
    #### GET INE PAGE ####
    ine_lista_page = requests.get("https://listanominal.ine.mx/scpln/")
    soup = BeautifulSoup(ine_lista_page.content, 'html.parser')

    #### CHECK IF CAPTCHAS ARE EQUAL ####
    all_captchas = soup.find_all('div', class_='g-recaptcha', attrs='data-sitekey')

    data_sitekeys = list()
    for i in range(len(all_captchas)):
        data_sitekeys.append(all_captchas[i].attrs['data-sitekey'])

    if all(x == data_sitekeys[0] for x in data_sitekeys):
        site_key = all_captchas[0].attrs['data-sitekey']
        ##### CAPTCHA SOLUTION ####
        url_ine = 'https://listanominal.ine.mx/scpln/'
        client = AnticaptchaClient(API_KEY)
        task = NoCaptchaTaskProxylessTask(url_ine, site_key)
        job = client.createTask(task)
        job.join()
        hashed_key = job.get_solution_response()
    else:
        ##### CAPTCHA SOLUTION ####
        url_ine = 'https://listanominal.ine.mx/scpln/'
        client = AnticaptchaClient(API_KEY)
        hashed_keys = list()

        for site_key in data_sitekeys:
            task = NoCaptchaTaskProxylessTask(url_ine, site_key)
            job = client.createTask(task)
            job.join()
            hashed_keys.append(job.get_solution_response())

    ##### FORMS ####
    if id_dict["tipo"] == 'a':
        parametros = {
            'modelo': 'a',
            'claveElector': id_dict["cve_elec"],
            'numeroEmision': id_dict["num_emis"], # 2 digitos 00, 01
            'ocr': id_dict["ocr_v"], #13 digitos
            "g-recaptcha-response": hashed_key
        }

        ##### POST ####
        pg_out = requests.post(url='https://listanominal.ine.mx/scpln/resultado.html',
                               data=parametros)
        resp = BeautifulSoup(pg_out.text, 'html.parser')
        return resp.content

    if id_dict["tipo"] == 'd':
        parametros = {
            'modelo':	'd',
            'cic': id_dict["cic"][:9], # 9 digitos después de IDMEX
            'ocr': id_dict["ocr_h"], # 13 ultimos digitos de 1er renglon
            'g-recaptcha-response': hashed_key}

        ##### POST ####
        pg_out = requests.post(url='https://listanominal.ine.mx/scpln/resultado.html',
                               data=parametros)
        resp = BeautifulSoup(pg_out.text, 'html.parser')
        return resp.content
    if id_dict["tipo"] == 'e':
        # en id_ciud 9 o 10 últimos digitos 1er renglon,
        # ojo hay diferentes longitudes en las cadenas
        parametros = {
            'modelo':	'e',
            'cic': id_dict["cic"][:9], # 9 digitos después de IDMEX
            'idCiudadano':id_dict["id_ciud"][5:13],
            'g-recaptcha-response': hashed_key}

        ##### POST ####
        pg_out = requests.post(url='https://listanominal.ine.mx/scpln/resultado.html',
                               data=parametros)
        #para modelos d y e el resultado se va a resultado.html
        resp = BeautifulSoup(pg_out.text, 'html.parser')
        return resp.content
    return resp

def proc_web_response(content):
    """
    Receives a raw HTML response from INE and extracts if the ID is valid
    as a Boolean value, returns its input and the extracted value as a
    dictionary
    """
    resp_dict = {"Error":"Please provide better images"}
    if content is not None:
        extracted_response = content
        valid_yn = [content.find_all('div', {'class': 'col-md-12'}),
                    content.find_all('table', {'class': 'table'})]
        return {"response": extracted_response, "valid": valid_yn}
    return resp_dict

def check_id_text(text_dict):
    """
    Function to query the INE page with a text dictionary it breaks the
    captcha using Anticaptcha
    INPUT: dictionary of fields as strings
    OUTPUT: response as list [html, validyn(string)]
    """
    return_dict = {"Error": "Problem calling INE"}
    response = query_web(text_dict)
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
    return_dict = check_id_text(processed_text)
    return return_dict
