import numpy as np
import pandas as pd
from preprocess_text.preproces_tsv import tsv_prep
import os
import re

dir_path = '/home/ferhdzschz/sandbox/projects/datavio/notebooks/lime/ocr/'
ocr_files = os.listdir(dir_path)

tsv_files = [s for s in ocr_files if "tsv" in s]
tsv_files.sort()

samples  =  np.unique(np.array([str(s).split(sep='_')[0] for s in tsv_files]))
samples  = samples.tolist()

assesed_tsv = pd.DataFrame()
i = 0

for sample in samples:
    i += i 
    print(str(sample) + ', {}'.format(str(i)))    
    r = re.compile('^{}_'.format(str(sample)))
    matches = list(filter(r.match, tsv_files))


    tsv_front_name  = matches[0]
    tsv_front_name = str(dir_path) + str(tsv_front_name)
    
    try:
      tsv_back_name = matches[1]
      tsv_back_name = str(dir_path) + str(tsv_back_name)
    except:
      tsv_back_name = tsv_front_name

    tsv_front = pd.read_csv(tsv_front_name , sep=r'\t', dtype={'text': str}, engine='python')
    tsv_back = pd.read_csv(tsv_back_name, sep=r'\t', dtype={'text': str}, engine='python')
    
    tsv = tsv_prep(tsv_front, tsv_back)
    prep_text = tsv.preprocess()
    prep_text['sample'] = sample

    assesed_tsv['{}_IFE'.format(str(sample))] = prep_text


final_df = assesed_tsv.T
final_df.to_csv('/home/ferhdzschz/sandbox/projects/datavio/notebooks/lime/assesed_ocr.csv', index = True)