import face_recognition
import os
import cv2 as cv
import sys
import multiprocessing
from multiprocessing import Pool
#from time import sleep


face_to_search_for_location = "/home/noah/Documents/software_mp/test data/img2.jpg"
images_to_search_location = "/home/noah/Documents/software_mp/test data/"

#declare the action variable
action = ''

video_file_location = '/home/noah/Videos/Last.Week.Tonight.with.John.Oliver.S10E15.720p.WEB.h264-EDITH.mkv'

#load overlay image
overlay_location = "/home/noah/Documents/software_mp/Laughing_man.png"

# Define the codec and create VideoWriter object
#fourcc = cv.VideoWriter_fourcc(*'XVID')
#out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

# Lists to store the results
images_that_match = []
images_that_do_not_match = []

directories = []

scale_factor = 0.35

def blur(image_bgr, target_face_location, used_kcf, scale_factor):
    # Unpack the location
    if used_kcf == False:
        top, right, bottom, left = target_face_location
        # Scale face_location coordinates up to the original image size
        top = int(top / scale_factor)
        right = int(right / scale_factor)
        bottom = int(bottom / scale_factor)
        left = int(left / scale_factor)
        # Calculate the width and height of the bounding box
        width = right - left
        height = bottom - top
    #Because KCF returns (x, y, width, height)
    elif used_kcf == True:
        x, y, width, height = target_face_location
        top = y
        left = x
        bottom = y + height
        right = x + width
    # Increase the region slightly to make sure the entire face is covered
    top = max(top - 10, 0)
    right = min(right + 10, image_bgr.shape[1])
    bottom = min(bottom + 10, image_bgr.shape[0])
    left = max(left - 10, 0)

    # Select the region of interest (ROI) where the face is located
    face_roi = image_bgr[top:bottom, left:right]

    # Apply a Gaussian blur to the face region
    blurred_face = cv.GaussianBlur(face_roi, (99, 99), 0)

    # Replace the original image region with the blurred face
    image_bgr[top:bottom, left:right] = blurred_face

    return image_bgr

def replace(background, overlay, target_face_location, used_kcf, scale_factor):
    # Unpack the location
    if used_kcf == False:
        top, right, bottom, left = target_face_location
        # Scale face_location coordinates up to the original image size
        top = int(top / scale_factor)
        right = int(right / scale_factor)
        bottom = int(bottom / scale_factor)
        left = int(left / scale_factor)
        # Calculate the width and height of the bounding box
        width = right - left
        height = bottom - top
    #Because KCF returns (x, y, width, height)
    elif used_kcf == True:
        x, y, width, height = target_face_location
        top = y
        left = x
        bottom = y + height
        right = x + width

    # Expand the bounding box by the constant value
    top = max(0, top - 10)
    bottom = min(background.shape[0], bottom + 10)
    left = max(0, left - 10)
    right = min(background.shape[1], right + 10)
    width = width + 20
    height = height + 20

    # Ensure the width and height are positive before resizing
    if width > 0 and height > 0:
        overlay_resized = cv.resize(overlay, (width, height))
    else:
        # Handle the invalid size case, e.g., by skipping the resizing or setting a default size
        print(f"Invalid size for resize operation: width={width}, height={height}")
        return background 

    # Check if overlay image has an alpha channel (transparency)
    if overlay_resized.shape[2] == 4:
        # Split overlay into color and alpha channels
        overlay_color = overlay_resized[:, :, :3]
        alpha_mask = overlay_resized[:, :, 3] / 255.0

        # Get the ROI from the background and blend using the alpha mask
        roi = background[top:bottom, left:right]
        roi = cv.addWeighted(overlay_color, alpha_mask, roi, 1 - alpha_mask, 0, roi)

        # Put the blended ROI back into the background
        background[top:bottom, left:right] = roi
    else:
        # If no alpha channel, just replace the ROI with the resized overlay
        background[top:bottom, left:right] = overlay_resized

    return background


def __init__():
    global overlay, face_to_search_for, face_to_search_for_encoding, action
    action = input("what do you want to do to matching images? 1: blur, 2 replace face: ")
    try:
        action = int(action)
    except:
        print("enter a valid number")
        exit()
    try:
        # Load the image containing the face you want to look for
        face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
        face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]
        if action == 2:
            #if selected access the overlay image
            overlay = cv.imread(overlay_location)
    except:
        print("Error accessing images containg face to search for, please try again")
    video = int(input("Do you want to run the program on video or photos (1 = video, 2 = photos): "))
    if int(video) == 1:
        live = live = input("Do you want to run the program on live video (y/n): ")
        if live.lower() == 'n':
            video_pre_recorded()
        else:
            video_live()
    
    if video == 2:
        # Get list of all files in the directory specified
        images_to_search = get_files(images_to_search_location)
        for dir in directories:
            images_to_search.append(get_files(dir))                

        with Pool(processes=multiprocessing.cpu_count()) as pool:
            # Map the image processing function over the images
            results = pool.map(face_recog, images_to_search)
        results = [item for item in results if item is not None]
        print(f"Done with images search. {len(results)} matches found.")
        # Optionally display matched images
        print(results)
        display = input("Do you want to view the images that match? (y/n): ")
        if display.lower() == "y":
            display_image(results)
    
def get_files(images_to_search_location):
    global directories
    images_to_search = os.listdir(images_to_search_location)
    for image_location in images_to_search:
        is_dir = os.path.isdir(image_location)
        if is_dir == True:
            directories.append(os.path.join(images_to_search_location, image_location))
            images_to_search.remove(image_location)
    images_to_search = [os.path.join(images_to_search_location, x) for x in images_to_search]
    return images_to_search



def video_live():
    cap = cv.VideoCapture(0)
    tracker = cv.TrackerCSRT_create()
    try:
        # Load the image containing the face you want to look for
        face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
        face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]
    except:
        print("Error accessing images containg face to search for, please try again")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    n = 5
    detected_face = False
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # operations on the frame come here
        try:
            if n == 5:
                used_kcf = False
                n = 0
                new_frame = frame
                small_frame = cv.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)
                # Load and run face recognition on the image to search
                frame_encodings = face_recognition.face_encodings(small_frame)
                if frame_encodings:
                    image_encoding = frame_encodings[0]
                    # Compare faces
                    results = face_recognition.compare_faces([face_to_search_for_encoding], image_encoding)
                    if results[0]:
                        detected_face = True
                        # Get location of faces in image
                        target_face_locations = face_recognition.face_locations(small_frame)
                        for target_face_location in target_face_locations:
                            # See if the face is a match for the known face
                            target_face_encoding = face_recognition.face_encodings(small_frame, [target_face_location])[0]
                            match = face_recognition.compare_faces([face_to_search_for_encoding], target_face_encoding)
                            converted_face_location = target_face_location
                            top, right, bottom, left = converted_face_location
                            top = int(top / scale_factor)
                            right = int(right / scale_factor)
                            bottom = int(bottom / scale_factor)
                            left = int(left / scale_factor)
                            # Convert from (top, right, bottom, left) to (x, y, width, height)
                            x, y, w, h = left, top, right - left, bottom - top
                            # Before initializing the tracker, ensure target_face_location is a tuple
                            if isinstance(target_face_location, tuple) and len(target_face_location) == 4:
                                tracker = cv.TrackerCSRT_create()
                                tracker.init(frame, (x, y, w, h))
                            else:
                                # Handle the error or re-initialize target_face_location
                                print("target_face_location is not a tuple with four elements")
                            # If it's a match, blur the face
                            new_frame = frame
                            if match[0]:
                                if action == 1:
                                    new_frame = blur(frame, target_face_location, used_kcf, scale_factor)
                                elif action == 2:
                                    new_frame = replace(frame, overlay, target_face_location, used_kcf, scale_factor)
                    else:
                        new_frame = frame
                        used_kcf = True
                        if detected_face == True:
                            if frame is not None:
                                update_result = tracker.update(frame)
                            else:
                                print("Frame is empty.")
                            if isinstance(update_result, tuple) and len(update_result) == 2:
                                success, target_face_location = update_result
                                if success:
                                    top, right, bottom, left = target_face_location
                                    x, y, w, h = tuple(map(int, target_face_location))
                                    #cv.rectangle(frame, target_face_location, (0, 255, 0), 2)
                                    if action == 1:
                                        new_frame = blur(frame, target_face_location, used_kcf, 1)
                                    elif action == 2:
                                        new_frame = replace(frame, overlay, target_face_location, used_kcf, 1)
                else:
                    new_frame = frame
            else:
                n = n + 1
                new_frame = frame
                used_kcf = True
                if detected_face == True:
                    if frame is not None:
                        update_result = tracker.update(frame)
                    else:
                        print("Frame is empty.")
                    if isinstance(update_result, tuple) and len(update_result) == 2:
                        success, target_face_location = update_result
                        if success:
                            top, right, bottom, left = target_face_location
                            x, y, w, h = tuple(map(int, target_face_location))
                            #cv.rectangle(frame, target_face_location, (0, 255, 0), 2)
                            if action == 1:
                                new_frame = blur(frame, target_face_location, used_kcf, 1)
                            elif action == 2:
                                new_frame = replace(frame, overlay, target_face_location, used_kcf, 1)
        

        except Exception as e:
            print(f"An error occurred with frame: {e}")
            # Display the resulting frame
        cv.namedWindow('frame', cv.WINDOW_NORMAL)
        cv.resizeWindow('frame', 1000, 900)
        cv.imshow('frame', new_frame)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows() 

def video_pre_recorded():
    cap = cv.VideoCapture(video_file_location)
    try:
        # Load the image containing the face you want to look for
        face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
        face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]
    except:
        print("Error accessing images containg face to search for, please try again")
    if not cap.isOpened():
        print("Cannot open file")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # operations on the frame come here
        try:
            used_kcf = False
            new_frame = frame
            # Load and run face recognition on the image to search
            frame_encodings = face_recognition.face_encodings(frame)
            if frame_encodings:
                image_encoding = frame_encodings[0]
                # Compare faces
                results = face_recognition.compare_faces([face_to_search_for_encoding], image_encoding)
                if results[0]:
                    # Get location of faces in image
                    target_face_locations = face_recognition.face_locations(frame)
                    for target_face_location in target_face_locations:
                        # See if the face is a match for the known face
                        target_face_encoding = face_recognition.face_encodings(frame, [target_face_location])[0]
                        match = face_recognition.compare_faces([face_to_search_for_encoding], target_face_encoding)                        
                        if match[0]:
                            if action == 1:
                                new_frame = blur(frame, target_face_location, used_kcf, 1)
                            elif action == 2:
                                new_frame = replace(frame, overlay, target_face_location, used_kcf, 1)
                else:
                    new_frame = frame
            else:
                new_frame = frame
        

        except Exception as e:
            print(f"An error occurred with frame: {e}")
        #write the resulting frame
        out.write(frame)
        # Display the resulting frame
        cv.namedWindow('frame', cv.WINDOW_NORMAL)
        cv.resizeWindow('frame', 1000, 900)
        cv.imshow('frame', new_frame)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    out.release()
    cv.destroyAllWindows()       

def display_image(images_that_match):
    for image_name in images_that_match:
        image_path = os.path.join(images_to_search_location, image_name)
        image = cv.imread(image_path)
        if image is None:
            sys.exit("Could not read the image.")
         # Get the size of the image
        height, width = image.shape[:2]

        # Define the window size
        max_height = 800
        max_width = 600

        # Calculate the ratio of the width and construct the dimensions
        if height > max_height or width > max_width:
            scaling_factor = max_height / float(height)
            if max_width/float(width) < scaling_factor:
                scaling_factor = max_width / float(width)
            # Resize the image
            image = cv.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_AREA)

        cv.imshow("Display window", image)
        k = cv.waitKey(0)
        cv.destroyAllWindows()
        if k == ord("s"):
            exit()


def face_recog(image_name):
    try:
        # Load and run face recognition on the image to search
        image = face_recognition.load_image_file(image_name)
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
                    # Put progress update to the queue
                    #progress_queue.put(1)
                    return image_name

            else:
                # Put progress update to the queue
                progress_queue.put(1)
                return f"Image {image_name} doesn't match"
        else:
            # Put progress update to the queue
            progress_queue.put(1)
            return f"No faces found in image {image_name}"
    
    except Exception as e:
        progress_queue.put(1)
        return f"An error occurred with image {image_name}: {e}"

# Run the face recognition
if __name__ == '__main__':
    __init__()
