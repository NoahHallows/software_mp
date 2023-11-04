import face_recognition
import os
import cv2 as cv
import sys


face_to_search_for_location = "/home/noah/Documents/software_mp/test data/img2.jpg"
images_to_search_location = "/home/noah/Documents/software_mp/test data/"

#ask user what they want to do to matching images
action = input("what do you want to do to matching images? 1: blur, 2 replace face: ")
try:
    action = int(action)
except:
    print("enter a valid number")
    exit()
# Load the image containing the face you want to look for
face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]

#load overlay image
overlay_location = "/home/noah/Documents/software_mp/Laughing_man.png"



# Lists to store the results
images_that_match = []
images_that_do_not_match = []

def blur(image_bgr, target_face_location):
    # Unpack the location
    top, right, bottom, left = target_face_location

    # Increase the region slightly to make sure the entire face is covered
    top = max(top - 10, 0)
    right = min(right + 10, image_bgr.shape[1])
    bottom = min(bottom + 10, image_bgr.shape[0])
    left = max(left - 10, 0)

    # Select the region of interest (ROI) where the face is located
    face_roi = image_bgr[top:bottom, left:right]

    # Apply a Gaussian blur to the face region
    blurred_face = cv.GaussianBlur(face_roi, (199, 199), 0)

    # Replace the original image region with the blurred face
    image_bgr[top:bottom, left:right] = blurred_face

    return image_bgr

def replace(background, overlay, target_face_location):
    # Unpack the location
    top, right, bottom, left = target_face_location
    # Calculate the width and height of the bounding box
    width = right - left
    height = bottom - top

    # Resize overlay image to match the bounding box size
    overlay_resized = cv.resize(overlay, (width, height))

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



def face_recog():
    # Get list of all files in the directory specified
    images_to_search = os.listdir(images_to_search_location)
    if action == 2:
        overlay = cv.imread(overlay_location)

    for image_name in images_to_search:
        current_image_to_search_location = os.path.join(images_to_search_location, image_name)
        
        try:
            # Load and run face recognition on the image to search
            image = face_recognition.load_image_file(current_image_to_search_location)
            image_encodings = face_recognition.face_encodings(image)
            
            if image_encodings:
                image_encoding = image_encodings[0]
                # Compare faces
                results = face_recognition.compare_faces([face_to_search_for_encoding], image_encoding)
                
                # Convert image to BGR for OpenCV
                image_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                
                if results[0]:
                    print(f"Image {image_name} matches")
                    images_that_match.append(image_name)
                    # Get location of faces in image
                    target_face_locations = face_recognition.face_locations(image)
                    for target_face_location in target_face_locations:
                        # See if the face is a match for the known face
                        target_face_encoding = face_recognition.face_encodings(image, [target_face_location])[0]
                        match = face_recognition.compare_faces([face_to_search_for_encoding], target_face_encoding)
                        # If it's a match, blur the face
                        if match[0]:
                            if action == 1:
                                new_image = blur(image_bgr, target_face_location)
                            elif action == 2:
                                new_image = replace(image_bgr, overlay, target_face_location)
                            cv.imwrite(current_image_to_search_location, new_image)

                else:
                    print(f"Image {image_name} doesn't match")
                    images_that_do_not_match.append(image_name)
            else:
                print(f"No faces found in image {image_name}")

        except Exception as e:
            print(f"An error occurred with image {image_name}: {e}")

    print(f"Done with images search. {len(images_that_match)} matches found.")

def display_image():
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

# Run the face recognition
face_recog()

# Optionally display matched images
display = input("Do you want to view the images that match? (y/n): ")
if display.lower() == "y":
    display_image()