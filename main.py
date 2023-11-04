import face_recognition
import os

face_to_search_for_location = input("Enter the location of the image containg the face you want to look for: ")
images_to_search_location = input("Enter the location of the images you want to search: ")
#face_to_search_for_location = "/home/noah/Documents/software_mp/test data/img2.jpg"
#images_to_search_location = "/home/noah/Documents/software_mp/test data/"


face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]


def face_recog():
    global face_to_search_for_encoding, images_to_search
    n = 1
    images_to_search = os.listdir(images_to_search_location)
    while n < len(images_to_search):
        try:
            current_image_to_search_location = images_to_search_location + images_to_search[n]
            image = face_recognition.load_image_file(current_image_to_search_location)
            image_encoding = face_recognition.face_encodings(image)[0]
            results = face_recognition.compare_faces([face_to_search_for_encoding], image_encoding)
            if results == [True]:
                print(f"Image {images_to_search[n]} matchs")
            else:
                print(f"Image {images_to_search[n]} doesn't match")
        except:
            print(f"Face recognition failed on image {images_to_search[n]}")
        n = n + 1
    print(f"Done with {n} images searched")

face_recog()