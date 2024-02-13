#PICTURE FACE DETECTION
import face_recognition
import cv2 as cv
import os
from multiprocessing import Pool, cpu_count, Queue
import editing_image


directories = []
images_to_search = []
action = 1
face_to_search_for_encoding = []
overlay = []

# Initialize a multiprocessing Queue for progress updates
#progress_queue = Queue()

def start_face_recognition(face_to_search_for_location, action_passed, overlay_location):
    global action, overlay, face_to_search_for_encoding, image_to_search
    action = action_passed     
    #Process the image contaning the face to search for
    face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
    face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]
    if action == 2:
        #if selected access the overlay image
        overlay = cv.imread(overlay_location)          

    with Pool(processes=cpu_count()) as pool:
        # Map the image processing function over the images
        results = pool.map(face_recog, images_to_search)
    results = [item for item in results if item is not None]
    return results

def get_files(images_to_search_location):
    global images_to_search
    images_to_search = []
    directories = []

    for item in os.listdir(images_to_search_location):
        item_path = os.path.join(images_to_search_location, item)

        if os.path.isdir(item_path):
            directories.append(item_path)
            images_to_search.extend(get_files(item_path))  # Recursively get files from subdirectories
        else:
            images_to_search.append(item_path)

    return images_to_search

def face_recog(image_name):
    print("1")
    used_kcf = False
    try:
        # Load and run face recognition on the image to search
        print("2")
        image = face_recognition.load_image_file(image_name)
        print("3")
        image_encodings = face_recognition.face_encodings(image)
            
        if image_encodings:
            image_encoding = image_encodings[0]
            # Compare faces
            results = face_recognition.compare_faces([face_to_search_for_encoding], image_encoding)
                
            # Convert image to BGR for OpenCV
            image_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)
            if results[0]:
                # Get location of faces in image
                target_face_locations = face_recognition.face_locations(image)
                for target_face_location in target_face_locations:
                    # See if the face is a match for the known face
                    target_face_encoding = face_recognition.face_encodings(image, [target_face_location])[0]
                    match = face_recognition.compare_faces([face_to_search_for_encoding], target_face_encoding)
                    # If it's a match, blur the face
                    if match[0]:
                        if action == 1:
                            new_image = editing_image.blur(image_bgr, target_face_location, used_kcf, 1)
                        elif action == 2:
                            new_image = editing_image.replace(image_bgr, overlay, target_face_location, 1)
                        new_image_name = "." + image_name + ".temp"
                        cv.imwrite(new_image_name, new_image)
                    return image_name

            else:
                # Put progress update to the queue
                return f"Image {image_name} doesn't match"
        else:
            # Put progress update to the queue
            return f"No faces found in image {image_name}"

    except Exception as e:
        return f"An error occurred with image {image_name}: {e}"