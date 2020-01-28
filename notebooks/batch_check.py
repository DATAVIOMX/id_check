from complete_validation import comp_process
import re
import os
import numpy as np
import string
import datetime
import pickle 
import sys 
import pandas as pd

def main():
    #Paths & Files
    dir_path = '/home/ferhdzschz/sandbox/projects/datavio_files/lime/2nd_dataset/images2/'
    filenames = os.listdir('/home/ferhdzschz/sandbox/projects/datavio_files/lime/2nd_dataset/images2')
    filenames.sort()
    fnames_index = np.unique(np.array([int(str(s).split(sep='_')[0]) for s in filenames]))

    list_info = []

    strt_time = datetime.datetime.now()
    print(strt_time)

    for fname_index in list(fnames_index):
        print('###### \n Image_no: {}'.format(fname_index))
        regex = re.compile("{}_.*".format(str(fname_index)))
        f_ext = list(filter(regex.match, filenames))[0].split('.')[-1:][0]
        f_list = list(filter(regex.match, filenames))
        fside_path = dir_path + list(filter(re.compile('.*front').match, f_list))[0]
        rside_path = dir_path + list(filter(re.compile('.*reverse').match, f_list))[0]
        if f_ext != "pdf":
            try:
                img_id = comp_process.id_all_flow(fside_path, rside_path, [500, 800], [500, 800])
                response_id = img_id.id_wrapper()
                list_response = [fname_index, img_id.data_dict, response_id]
                list_info.append(list_response)
            except:
                print('Exception found in {} file'.format(str(fname_index)))

    for fname_index in list(fnames_index):   
        regex = re.compile("{}_.*".format(str(fname_index)))
        f_ext = list(filter(regex.match, filenames))[0].split('.')[-1:][0]
        if f_ext == 'pdf':
            fname_index



    end_time = datetime.datetime.now()
    print(end_time)
    total_time = end_time-strt_time
    print(total_time)

    nums_in_list = set([inf[0] for inf in list_info])
    total_nums = set(range(1,300))

    list_info
    total_nums - nums_in_list


    sys.setrecursionlimit(100000) 

    with open('/home/ferhdzschz/sandbox/projects/datavio_files/lime/2nd_dataset/info_creds_3.pickle','wb') as f:
        pickle.dump(list_info, f)


if __name__ == '__main__':
    main()