from bs4 import BeautifulSoup
import requests
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
import pandas as pd

class consulta_id():
    '''
    Class for checking validity of id
    ----------------------------------

    Params:
    -------
    id_data: series or data.frame containig all the information from a id.

    Methods:
    --------
    ine_check(api_key): uses anticaptcha service to solve the recaptcha and provide a captcha key to fill the request form

    '''


    
    def __init__(self, id_data):
      self.cve_elec = id_data['cve_elec']
      self.num_emis = id_data['emision']
      self.ocr_v = id_data['ocr_vertical']
      self.ocr_h = id_data['ocr_horizontal']
      self.cic = id_data['cic']
      self.id_ciud = id_data['cve_ciudadano']
      self.tipo = id_data.loc[0,'tipo_cred']

    def ine_check(self, api_key):
      print("Tipo de IFE/INE {}:".format(self.tipo))
      #### GET INE PAGE ####
      ine_lista_page = requests.get("https://listanominal.ine.mx/scpln/")
      soup = BeautifulSoup(ine_lista_page.content, 'html.parser')

      #### CHECK IF CAPTCHAS ARE EQUAL ####
      all_captchas = soup.find_all('div', class_= 'g-recaptcha', attrs='data-sitekey')

      data_sitekeys = list()
      for i in range(len(all_captchas)):
          data_sitekeys.append(all_captchas[i].attrs['data-sitekey'])

      if all(x == data_sitekeys[0] for x in data_sitekeys):
          print("All the data-sitekeys are identical")
          captcha_site_key = all_captchas[0].attrs['data-sitekey']
          ##### CAPTCHA SOLUTION ####
          site_key =  captcha_site_key # grab from site
          url_ine = 'https://listanominal.ine.mx/scpln/'

          client = AnticaptchaClient(api_key)
          task = NoCaptchaTaskProxylessTask(url_ine, site_key)
          job = client.createTask(task)
          job.join()
          hashed_key = job.get_solution_response()
      else:
          print("All the data-sitekeys are not identical") #For every data-site-key solve captcha
          ##### CAPTCHA SOLUTION ####
          url_ine = 'https://listanominal.ine.mx/scpln/'
          client = AnticaptchaClient(api_key)
          hashed_keys  = list()
        
          for site_key in data_sitekeys:
              task = NoCaptchaTaskProxylessTask(url_ine, site_key)
              job = client.createTask(task)
              job.join()
              hashed_keys.append(job.get_solution_response())
      
      ##### FORMS ####
      if self.tipo == 'a':

          parametros = {
            'modelo': 'a',
            'claveElector': self.cve_elec, # 18 caracteres 
            'numeroEmision': self.num_emis, # 2 digitos 00, 01
            'ocr': self.ocr_v, #13 digitos
            "g-recaptcha-response": hashed_key
          }

          ##### POST ####
          response = requests.post(url = 'https://listanominal.ine.mx/scpln/resultado.html', data= parametros) #para modelos d y e el resultado se va a resultado.html
          #response = requests.post(url = 'https://listanominal.ine.mx/scpln/', data= parametros) #para modelo a el resultado se va a resultado.html
          output = BeautifulSoup(response.text, 'html.parser')      
      elif self.tipo == 'd':
          parametros = {
          'modelo':	'd',
          'cic': self.cic[0:9], # 9 digitos después de IDMEX
          'ocr': self.ocr_h, # 13 ultimos digitos de 1er renglon
          'g-recaptcha-response': hashed_key	
          }

          ##### POST ####
          response = requests.post(url = 'https://listanominal.ine.mx/scpln/resultado.html', data= parametros) #para modelos d y e el resultado se va a resultado.html
          output = BeautifulSoup(response.text, 'html.parser')      
      elif self.tipo == 'e':
          parametros = {
          'modelo':	'e',
          'cic': self.cic[0:9], # 9 digitos después de IDMEX
          'idCiudadano':self.id_ciud[5:13], # 9 últimos digitos 1er renglon
          'g-recaptcha-response': hashed_key
          }

          ##### POST ####
          response = requests.post(url = 'https://listanominal.ine.mx/scpln/resultado.html', data= parametros) #para modelos d y e el resultado se va a resultado.html
          output = BeautifulSoup(response.text, 'html.parser')
      
      return(output)

    def check_curp(self):
      pass







