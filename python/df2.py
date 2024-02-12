#calling the dependencies
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt 

#importing the images
img1_path = ''
img2_path = 'https://8f430952.rocketcdn.me/content/Img2.jpg'
img3_path = 'https://8f430952.rocketcdn.me/content/Img3.jpg'
#confirming the path of images
img1 = cv2.imread(img1_path)
img2 = cv2.imread(img2_path) 

plt.imshow(img1[:, :, ::-1 ]) #setting value as -1 to maintain saturation
plt.show()
plt.imshow(img2[:, :, ::-1 ])
plt.show() 

#calling VGGFace
model_name = "VGG-Face"
model = DeepFace.build_model(model_name) 

result = DeepFace.verify(img1_path,img2_path)#validate our images
DeepFace.verify("Img1.jpg","Img2.jpg")#generating result of comparison 
