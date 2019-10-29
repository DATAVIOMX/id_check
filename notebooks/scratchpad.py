from notebooks.check_id import web_search
from notebooks.preprocess_text import preproces_tsv
import pandas as pd
import numpy as np
import os
import re
import xlrd
from bs4 import BeautifulSoup

#proj_dir = '/home/ferhdzschz/sandbox/projects/datavio/notebooks/'
#
#tsv_1 = pd.read_csv(proj_dir + 'ifes_ocr/2_front.tsv', sep='\t')
#tsv_2 = pd.read_csv(proj_dir + 'ifes_ocr/2_back.tsv', sep='\t')
#
#x = preproces_tsv.tsv_prep(tsv_1, tsv_2)
#
#test_list = x.join_tsv()
#tipo_cred = x.identify_cardtype(test_list)
#
#

tsv_completo = pd.read_excel('/home/ferhdzschz/Downloads/revision_manual.xlsx', sheet_name=4)

pruebas = tsv_completo.loc[(tsv_completo['tipo_cred'] == 'e') & (tsv_completo['cic'] != 'NOT DETECTED'), :]

test = pruebas.iloc[22]
respuestas = []

for i in range(3,100):       
    test = pruebas.iloc[i]
    w_s = web_search.consulta_id(test)
    response = w_s.ine_check('f93c8b9646c63020ef084ecac088583d')
    otuput = [test['sample'], response.find('p', {'class': 'lead'})]
    respuestas.append(otuput)

respuestas[9]  
#indexes_CLAVE = [i for i,x in enumerate(test_list) if x == 'CLAVE']
#indexes_DE = [i for i,x in enumerate(test_list) if x == 'DE']
#index_ELECTOR = test_list.index("ELECTOR")
#ndexes_CLAVE[indexes_CLAVE.index(index_ELECTOR-2)]
#indexes_DE[indexes_DE.index(index_ELECTOR-1)]

#CVE ELECTOR
regex_find = re.compile(r"\w{6}\d{8}\w\d{3}")
list(filter(regex_find.search, test_list))[0]

regex_find = re.compile(r"REGISTRO")
registro_index = [i for i,x in enumerate(test_list) if x == list(filter(regex_find.search, test_list))[-1]][-1]
test_list[registro_index+1]
test_list[registro_index+2]

if len(test_list[registro_index+1]) >= 7:
    print(test_list[registro_index+1][-2:])
elif len(test_list[registro_index+1]) == 4:
    print(test_list[registro_index+2])

#CURP
regex_find = re.compile(r"\w{4}\d{6}\w{6}\d{2}|\w{4}\d{6}\w{8}")
list(filter(regex_find.search, test_list))


HESF 910629 HDFRNR 08 , HRSNFR 91062909 H 300
GARV 880310 MNERVC 00 , GRRVVC 88031088 M 400,
PEMM 900126 HMCRLN 06 , PMRLMN 90012615 H 600
CEVA 930217 HDFRRN 00 , CRVRAN 83021709 H 800
AACJ 840113 HDFRRR 08 , ARCRJR 84011309 H 400