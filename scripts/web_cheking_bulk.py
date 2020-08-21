from notebooks.check_id import web_search
from notebooks.preprocess_text import preproces_tsv
import pandas as pd
import numpy as np
import os
import re
import xlrd
from bs4 import BeautifulSoup
from bs4 import Comment
import string
import datetime
import time

#Load output file from assesment_tsv
tsv_completo = pd.read_excel('/home/ferhdzschz/Downloads/revision_manual.xlsx', sheet_name=4)

# Filter by most complete ids
pruebas = tsv_completo.loc[(tsv_completo['tipo_cred'] == 'e') & (tsv_completo['cic'] != 'NOT DETECTED'), :]

#Initiating web search
w_s = web_search.consulta_id(test)
respuestas = []
start_time = datetime.datetime.now()

#Loop aprox 40 segs to respond each captcha
for i in range(0, 4): 
    print("\n\n ##### Iteration: {} #####\n".format(str(i)))
    test = pruebas.iloc[i]
    w_s = web_search.consulta_id(test)
    response = w_s.ine_check('f93c8b9646c63020ef084ecac088583d')
    otuput = [test['sample'], 
              response.findAll('div',{'class': 'col-md-12'}),
              response.findAll('table',{'class': 'table'})]
    respuestas.append(otuput)
    time.sleep(.5)

print("Start time: {}\n".format(str(start_time)))
end_time = datetime.datetime.now()
print("End time: {}".format(str(end_time)))
total_time = end_time-start_time
print("Elapsed time: {}\n\n".format(str(total_time)))

