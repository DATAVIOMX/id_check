import re
from bs4 import BeautifulSoup
import requests
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

def query_web(id_dict):
    """
    Simple web caller that receives a dictionary of data, fills a form
    and calls the INE website, returns the HTML response
    """
    # print("id_dict", id_dict)
    if id_dict is None:
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
        client = AnticaptchaClient("f93c8b9646c63020ef084ecac088583d")
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
            'numeroEmision': id_dict["emision"], # 2 digitos 00, 01
            'ocr': id_dict["ocr_vertical"], #13 digitos
            "g-recaptcha-response": hashed_key
        }
        ##### POST ####
        pg_out = requests.post(url='https://listanominal.ine.mx/scpln/resultado.html',
                               data=parametros)
        resp = BeautifulSoup(pg_out.text, 'html.parser')
        return resp
    if id_dict["tipo"] == 'd':
        parametros = {
            'modelo': 'd',
            'cic': id_dict["cic"], # 9 digitos después de IDMEX
            'ocr': id_dict["ocr_horizontal"], # 13 ultimos digitos de 1er renglon
            'g-recaptcha-response': hashed_key}

        ##### POST ####
        pg_out = requests.post(url='https://listanominal.ine.mx/scpln/resultado.html',
                               data=parametros)
        resp = BeautifulSoup(pg_out.text, 'html.parser')
        return resp
    if id_dict["tipo"] == 'e':
        # en id_ciud 9 o 10 últimos digitos 1er renglon,
        # ojo hay diferentes longitudes en las cadenas
        print("id_dict", id_dict)
        parametros = {
            'modelo':'e',
            'cic': id_dict["cic"],
            'idCiudadano':id_dict["cve_elec"],
            'g-recaptcha-response': hashed_key}

        ##### POST ####
        pg_out = requests.post(url='https://listanominal.ine.mx/scpln/resultado.html',
                               data=parametros)
        #para modelos d y e el resultado se va a resultado.html
        resp = BeautifulSoup(pg_out.text, 'html.parser')
        return resp
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
        page = content.findAll(text=True)
        page_text = "".join(t.strip() for t in page)
        for frag in valid:
            text = ''.join(frag.findAll(text=True))
            if text.find("vigente"):
                return {"content":page_text, "valid_yn":"Y"}
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
    response = query_web(text_dict)
    print("response", response)
    if response:
        return_dict = proc_web_response(response)
        print("return_dict", return_dict)
    return return_dict
