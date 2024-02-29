from deepface import DeepFace as df

metrics = ["cosine", "euclidean", "euclidean_l2"]

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]

detectors = ["opencv", "ssd", "mtcnn", "dlib", "retinaface"]

model = models[6] 
model1 = df.build_model(model) 

result = df.verify("/home/noah/Documents/software_mp/test data/img2.jpg", "/home/noah/Documents/software_mp/test data/img1.jpg", detector_backend = "mtcnn", model_name = "Facenet" )

#find = df.find(img_path = "/home/noah/Documents/software_mp/test data/img2.jpg", db_path = "/home/noah/Documents/software_mp/test data/", model_name = model, distance_metric = metrics[2])
#obj = df.analyze(img_path = "/home/noah/Documents/software_mp/test data/img2.jpg", actions = ['age', 'gender', 'race', 'emotion'])
print(result)
