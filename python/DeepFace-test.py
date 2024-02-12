from deepface import DeepFace as df

metrics = ["cosine", "euclidean", "euclidean_l2"]

models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]

model = models[6] 
model1 = df.build_model(model) 

#find = df.find(img_path = "/home/noah/Documents/software_mp/test data/img2.jpg", db_path = "/home/noah/Documents/software_mp/test data/", model_name = model, distance_metric = metrics[2])
obj = df.analyze(img_path = "/home/noah/Documents/software_mp/test data/img2.jpg", actions = ['age', 'gender', 'race', 'emotion'])
print(obj)
