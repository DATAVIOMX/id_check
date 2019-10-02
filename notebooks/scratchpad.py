from notebooks.check_id import web_search
from notebooks.preprocess_text import preproces_tsv
import pandas as pd
import numpy as np
import os
import re

proj_dir = '/home/ferhdzschz/sandbox/projects/datavio/notebooks/'

tsv_1 = pd.read_csv(proj_dir + 'ifes_ocr/1_front.tsv', sep='\t')
tsv_2 = pd.read_csv(proj_dir + 'ifes_ocr/1_back.tsv', sep='\t')

x = preproces_tsv.tsv_prep(tsv_1, tsv_2)

test_list = x.join_tsv()
tipo_cred = x.identify_cardtype(test_list)
prueba = x.prep_text(test_list, tipo_cred)   

w_s = web_search.consulta_id(prueba)
w_s.ine_check('f93c8b9646c63020ef084ecac088583d')

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