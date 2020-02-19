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
8. proc_ocr_text() OK
9. query_web() OK
10. proc_web_response() OK (check)

"""
import re
from bs4 import BeautifulSoup
import requests
import cv2
import pytesseract
import imutils
# import numpy as np
# import string
# import os
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask


API_KEY = "f93c8b9646c63020ef084ecac088583d"
CVE_ELEC_RE = re.compile(r"\w{6}\d{8}\w\d{3}")

def get_qr(img):
    """
    Simple function that decodes a QR code from an image returns the URL
    inside the code or None (on failure)
    INPUT: image as cv2 image
    OUTPUT: url as string or None
    """
    url = None
    if img is not None:
        url = decode(img, symbols=[ZBarSymbol.QRCODE])[0].data.decode("utf-8")
    return url

def query_qr(url):
    """
    Simple method to query if a QR code from an INE is valid
    INPUT: url as string
    OUTPUT: response as list [html, valid]
    """
    if not url:
        return None
    try:
        response = requests.get(url)
        return response.content
    except ValueError:
        return None

def clean_qr_response(resp):
    """
    Cleanup function to extract the boolean value of valid ID from the
    HTML content of the response
    """
    if resp is None or resp == "":
        return None
    extracted_response = BeautifulSoup(resp, 'html.parser')
    valid_yn = extracted_response.find(name='div', id="menje")
    if valid_yn:
        return {"response": extracted_response, "valid": valid_yn}
    return None

def prep_img(img):
    """
    Image processing steps, this function receives an image and does the
    following:
    - binarization
    - Denoising
    - Filtering
    - Edge detection
    - Perspective warping
    It receives an image and returns the processed image as 4 images
    """
    if img is None:
        return None
    cv2.imshow("prep_img", img)
    cv2.waitKey(0)
    # Rotations
    rot_angles = [90, 180, 270]
    rot_imgs = [imutils.rotate_bound(img, x) for x in rot_angles]
    rot_imgs.insert(0, img)
    # greyscale
    gray = [cv2.cvtColor(x, cv2.COLOR_BGR2GRAY) for x in rot_imgs]
    # Gaussian Blur
    blurred = [cv2.GaussianBlur(x, (3, 3), 0) for x in gray]
    threshold = [cv2.threshold(x, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) for x in blurred]
    contours = [cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)]
    # Sort contours
    sorted_cnts = [sorted(imutils.grab_contours(x), key=cv2.contourArea,
                          reverse=True) for x in contours]
    # crop thresholded images to the largest contour
    contour_data = [[num_foto, cont_data, cont_data[2] / float(cont_data[3]),
                     cont_data[2] / float(threshold[num_foto].shape[1])]
                    for num_foto, cont_data in sorted_cnts]

    valid_contours = [[num_foto, cont_data, ar, crWidth] for num_foto,
                      cont_data, ar, crWidth in contour_data if ar >= 4]

    #coordinate for cropping images
    coord_rectangles = [[num_foto, int((cont_data[0] + cont_data[2]) * 0.03),
                         int((cont_data[1] + cont_data[3]) * 0.03),
                         cont_data[0] - int((cont_data[0] + cont_data[2]) * 0.03),
                         cont_data[1] - int((cont_data[1] + cont_data[3]) * 0.03),
                         cont_data[2] + (int((cont_data[0] + cont_data[2]) * 0.03) *2),
                         cont_data[3] + (int((cont_data[1] + cont_data[3]) * 0.03) *2)]
                        for num_foto, cont_data, ar, crWidth in valid_contours]
    #cropped images
    cropped = [threshold[num_foto][y:y + h, x:x + w] for num_foto,
               pX, pY, x, y, w, h in coord_rectangles]
    return cropped

def ocr_img(imgs):
    """
    Calls tesseract on a processed image
    receives an image and returns a string
    """
    if imgs is None or imgs == []:
        return None
    all_text = ""
    for img in imgs:
        # text = pytesseract.image_to_string(img, lang="spa+eng")
        text = pytesseract.image_to_string(img)
        all_text += text
    return all_text

def proc_text(text, id_type):
    """
    Text processing routine, takes the OCR text and does extraction of
    relevant fields based on regexes
    INPUT: text, id_type
    OUTPUT: id_dict a dictionary with different information fields based
    on the ID type
    REVISAR
    """
    if text is None or id_type is None:
        return None
    lines = [y for y in (x.strip() for x in text.splitlines()) if y]
    cve_elector = None
    cic = ocr_h = None
    for line in lines:
        if CVE_ELEC_RE.match(line):
            cve_elector = CVE_ELEC_RE.findall(line)[0]
            continue
        if line.find('DMEX') != -1:
            cic, ocr_h = line.split('<<')
            cic = cic[-10:len(cic)]
            break
    ret_dict = {"tipo_cred": id_type, "cve_elec": cve_elector,
                "cic":cic, "ocr_horizontal":ocr_h}
    if ret_dict['cic'] is None and ret_dict['ocr_horizontal'] is None:
        return None
    return ret_dict

def get_id_type(text):
    """
    Classifier of IDs based on the text
    INPUT: text
    OUTPT: ID type (as a character), None on failure
    """
    if text is None:
        return None
    text = text.splitlines()
    if ((any('TO FEDERAL' in mystring for mystring in text)) and
            ((any('DMEX' in mystring for mystring in text)) or
             (any('IDMEX' in mystring for mystring in text)) or
             (any('0MEX' in mystring for mystring in text)))):
        return 'd'
    if(any('TO NACIONAL' in mystring for mystring in text) or
       any('TO NACION' in mystring for mystring in text)):
        return 'e'
    if(any('TO FEDERAL' in mystring for mystring in text) and
       ((any('DOCUMENTO' in mystring for mystring in text)) or
        (any('TACHA' in mystring for mystring in text)) or
        (any('ENMENDADURA' in mystring for mystring in text)) or
        (any('INTRANSFERIBLE' in mystring for mystring in text)))):
        return 'a'
    return None

def proc_ocr_text(text):
    """
    Receives a string and returns a dictionary containing the ID fields
    and the ID type
    """
    if text is None:
        return None
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
    if id_dict is None:
        return None
    if not any(elem in ["tipo", "cve_elec", "num_emis", "ocr_v"] for elem in id_dict.keys()):
        return None
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
            'cic': id_dict["cic"],
            'idCiudadano':id_dict["ocr_h"],
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
    if content is None:
        return None
    if content is not None:
        valid = content.findAll('h4')
        for frag in valid:
            text = ''.join(frag.findAll(text=True))
            if text.find("vigente"):
                return {"content":content, "valid_yn":"Y"}
    return None

def check_id_text(text_dict):
    """
    Function to query the INE page with a text dictionary it breaks the
    captcha using Anticaptcha
    INPUT: dictionary of fields as strings
    OUTPUT: response as list [html, validyn(string)]
    """
    return_dict = {"Error": "No response from server"}
    if text_dict is None:
        return {"Error": "Input is empty"}
    if not any(elem in ["tipo", "cve_elec", "num_emis", "ocr_h"] for elem in text_dict.keys()):
        return {"Error": "Invalid input"}
    response = query_web(text_dict)
    print("response", response)
    if response:
        return_dict = proc_web_response(response)
        print("return_dict", return_dict)
    return return_dict

def check_id_img(front, back):
    """
    Function that checks if an INE provided as two images (front and back)
    is valid through the ine website
    INPUT: front, back : Image as numpy array
    OUTPUT: string representation of HTML response from server
    """
    if front is None and back is None:
        return {"Error": "Input is empty"}
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
