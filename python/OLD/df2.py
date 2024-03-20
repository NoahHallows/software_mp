#calling the dependencies
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt 

#importing the images
img1_path = '/home/noah/Documents/software_mp/test data/img1.jpg'
img2_path = '/home/noah/Documents/software_mp/test data/img2.jpg'
#confirming the path of images
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path) 

#plt.imshow(img1[:, :, ::-1 ]) #setting value as -1 to maintain saturation
#plt.show()
#plt.imshow(img2[:, :, ::-1 ])
#plt.show() 

#calling VGGFace
model_name = "VGG-Face"
model = DeepFace.build_model(model_name) 

result = DeepFace.verify(img1_path,img2_path)#validate our images
DeepFace.verify(img1,img2)#generating result of comparison 
