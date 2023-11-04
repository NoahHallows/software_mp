import face_recognition
import os
import cv2 as cv
import sys


#face_to_search_for_location = input("Enter the location of the image containg the face you want to look for: ")
#images_to_search_location = input("Enter the location of the images you want to search: ")
face_to_search_for_location = "/home/noah/Documents/software_mp/test data/img2.jpg"
images_to_search_location = "/home/noah/Documents/software_mp/test data/"

#run face recogntion of image containg face to search for
face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]


images_that_match = []
images_that_do_not_match = []


def face_recog():
    global face_to_search_for_encoding, images_to_search, images_that_do_not_match, images_that_match
    n = 0
    #get list of all files in directory specified
    images_to_search = os.listdir(images_to_search_location)
    #run for all images found in directory
    while n < len(images_to_search):
        try:
            #add full file path
            current_image_to_search_location = images_to_search_location + images_to_search[n]
            #load and run face recogntion of image to search
            image = face_recognition.load_image_file(current_image_to_search_location)
            image_encoding = face_recognition.face_encodings(image)[0]
            #get location of faces in image
            target_face_locations = face_recognition.face_locations(image)
            #compare faces
            results = face_recognition.compare_faces([face_to_search_for_encoding], image_encoding)
            #convert image to bgr for opencv
            image_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)
            if results == [True]:
                print(f"Image {images_to_search[n]} matchs")
                images_that_match.append(images_to_search[n])
            else:
                print(f"Image {images_to_search[n]} doesn't match")
                images_that_do_not_match.append(images_to_search[n])

            
            for target_face_location in target_face_locations:
                # Get the face encoding for the current face in the target image
                top, right, bottom, left = target_face_location
                target_face_encoding = face_recognition.face_encodings(image, [target_face_location])[0]

                # See if the face is a match for the known face
                match = face_recognition.compare_faces([face_to_search_for_encoding], target_face_encoding)

                # If it's a match, blur the face
                if match[0]:
                    blur(image, target_face_location, current_image_to_search_location)
            
        except:
            print(f"Face recognition failed on image {images_to_search[n]}")
        n = n + 1
    print(f"Done with {n} images searched")
    display = input("do you want to view the images that match? (y/n): ")
    if display.lower() == "y":
        display_image()
    else:
        pass

def display_image():
    global images_that_do_not_match, images_that_match
    n = 0
    while n < len(images_that_match):
        image_path =  images_to_search_location + images_that_match[n]
        image = cv.imread(image_path)
        if image is None:
            sys.exit("Could not read the image.")

        window_name = images_that_match[n]
        #cv.destroyAllWindows()

        cv.imshow("Display window", image)
        k = cv.waitKey(0)
        cv.destroyAllWindows()
        if k == ord("s"):
            exit()
        n = n + 1

def blur(image, target_face_locaion, image_location):
    # Increase the region slightly to make sure the entire face is covered
    top -= 10
    right += 10
    bottom += 10
    left -= 10
    #convert image to bgr for opencv
    image_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    # Select the region of interest (ROI) where the face is located
    face_roi = image_bgr[top:bottom, left:right]

    # Apply a Gaussian blur to the face region
    blurred_face = cv.GaussianBlur(face_roi, (99, 99), 30)

    # Replace the original image region with the blurred face
    image_bgr[top:bottom, left:right] = blurred_face

    # Save the final image
    cv.imwrite(image_location, image_bgr)


face_recog()