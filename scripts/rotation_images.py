import pandas as pd
import imutils
from skimage import exposure
import numpy as np
import argparse
import cv2
import os
import re 
import math

#DIrectories

dir_folder = '/home/ferhdzschz/sandbox/projects/datavio/notebooks/lime/images/'
archivos = os.listdir(dir_folder)
rotations = pd.read_csv('/home/ferhdzschz/sandbox/projects/datavio/notebooks/lime/rotations.csv')

#ENcontrar extensiones y contarlas

extensiones = [str.split(filename, sep = '.')[1] for filename in archivos]
unicos, frecuencia = np.unique(np.array(extensiones), return_counts=True)
dict(zip(unicos, frecuencia))

#Find rotation
files_rotation = pd.DataFrame()
files_rotation['filename'] 

filenames = []

for i in range(0,1000):
		front_name = '{}_IFEfrontSide.{}'.format(str(rotations.loc[i, 'Sample']), str(rotations.loc[i, 'FormatFront']))
		front_rotation = rotations.loc[i, 'RotationFront']
		cred_type = rotations.loc[i, 'Tipo']

		filenames.append([front_name, front_rotation, cred_type])
		
		back_name = '{}_IFEreverseSide.{}'.format(str(rotations.loc[i, 'Sample']), str(rotations.loc[i, 'FormatReverse']))
		back_rotation = rotations.loc[i, 'RotationReverse']
		filenames.append([back_name, back_rotation, cred_type])

file_rotation = pd.DataFrame(filenames, columns= ('filename', 'rotation', 'card_type'))
file_rotation.groupby('card_type').count()

selected_files = file_rotation[file_rotation['filename'].str.contains('png|jp',flags=re.IGNORECASE, regex=True)]
selected_files = selected_files.reset_index(drop = True)

####### Rotate
for i in range(len(selected_files)):
		ife_name = str(selected_files.loc[i, 'filename'])
		print(ife_name)
		image = cv2.imread(dir_folder + str(selected_files.loc[i, 'filename']))
		if math.isnan(selected_files.loc[i, 'rotation']):
			rot = rotation_dict[1]
		else:
			rot = rotation_dict[selected_files.loc[i, 'rotation']]
		rotated_1 = imutils.rotate_bound(image, -rot)
		#cv2.imshow("Image", rotated_1)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		cv2.imwrite('/home/ferhdzschz/sandbox/projects/datavio/notebooks/lime/correct_imgs/{}'.format(ife_name), rotated_1)
