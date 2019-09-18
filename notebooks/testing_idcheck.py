from check_id import web_search 
import pandas as pd  
import numpy as np
from bs4 import BeautifulSoup
import requests

ine_data = pd.read_csv('list_id_data.csv')


test_data = ine_data.iloc[4]

test_data['emision'] = '0{}'.format(str(test_data.loc['emision']))
test_data

if test_data['tipo_cred'] == 'a':
  test_data['ocr_vertical'] = str(int(test_data.loc['ocr_vertical']))
elif test_data['tipo_cred'] == 'd':
  test_data['ocr_horizontal'] = str(int(test_data.loc['ocr_horizontal']))
  test_data['cic'] = str(int(test_data.loc['cic']))
elif test_data['tipo_cred'] == 'e':
  test_data['cve_ciudadano'] = str(int(test_data.loc['cve_ciudadano']))
  test_data['cic'] = str(int(test_data.loc['cic']))


id_check = web_search.consulta_id(test_data)

id_check.ine_check(api_key = 'f93c8b9646c63020ef084ecac088583d')
