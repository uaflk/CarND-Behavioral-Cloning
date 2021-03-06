import csv
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
import numpy as np
import os
import pickle

augment_factor = 0.1
resize_x = 64
resize_y = 32

images = []
steering_angles = []

csv_path = '/home/hanqiu/Udacity/CarND-Behavioral-Cloning/Record/mini/driving_log.csv'


with open(csv_path,'r') as csvfile:
	csv_reader = csv.reader(csvfile, delimiter=',',skipinitialspace=True)
	for csv_length,row in enumerate(csv_reader):
		pass
	csvfile.close()

with open(csv_path,'r') as csvfile:
	csv_reader = csv.reader(csvfile, delimiter=',',skipinitialspace=True)
	
	for row in tqdm(csv_reader,total=csv_length):
		for i in range(3):
			img = cv2.imread(row[i],cv2.IMREAD_COLOR)
			img = cv2.resize(img,dsize=(resize_x,resize_y))
			img = cv2.cvtColor(img,cv2.COLOR_BGR2Luv)
			img.shape += (1,)
			images.append(img[:,:,0])

			angle = float(row[3])
			if (i == 0):
				steering_angles.append(angle)
			elif (i == 1):
				angle = angle * (1 + np.sign(angle) * augment_factor)
				if (angle > 1):
					angle = 1
				elif (angle < -1):
					angle = -1
				elif (angle == 0):
					angle = augment_factor/2
				steering_angles.append(angle)
			elif (i == 2):
				angle = angle * (1 - np.sign(angle) * augment_factor)
				if (angle > 1):
					angle = 1
				elif (angle < -1):
					angle = -1
				elif (angle == 0):
					angle = -augment_factor/2
				steering_angles.append(angle)

	csvfile.close()

images_np = np.zeros((len(images),resize_y,resize_x,1),dtype=np.uint8)
steering_angles_np = np.zeros(len(images),dtype=np.float32)


for i in range(len(images)):
	images_np[i] = images[i]
	steering_angles_np[i] = steering_angles[i]

#print(type(images_np))
#print(images_np.shape)

pickle_file = 'mini_test_set.p'

print('Saving data to pickle file...')
try:
    with open('mini_test_set.p', 'wb') as pfile:
        pickle.dump(
            {
                'images': images_np,
                'angles': steering_angles_np,
            },
            pfile, pickle.HIGHEST_PROTOCOL)
except Exception as e:
    print('Unable to save data to', pickle_file, ':', e)
    raise

print('Data cached in pickle file.')

print (type(images_np[0,:,:,0]))
print (images_np[0,:,:,0].shape)

#plt.figure()
#plt.imshow(images[0],cmap='gray')
#plt.show()
fig = plt.figure(figsize=(15,15))

for i in range(9):
	sub = plt.subplot(3,3,i+1)
	plt.imshow(images_np[i,:,:,0],cmap='gray')
	sub.set_title('Steering angle: ' + str(steering_angles[i]))

plt.show()
