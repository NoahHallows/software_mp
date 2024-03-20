#VIDEO
import cv2 as cv
import face_recognition
import editing_image


def video_cap(face_to_search_for_location, performace, action, overlay_location):
    cap = cv.VideoCapture(0)
    tracker = cv.TrackerCSRT_create()
    #Process the image contaning the face to search for
    face_to_search_for = face_recognition.load_image_file(face_to_search_for_location)
    face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]
    if performace <= 1:
        scale_factor = 0.25
        tracking = True
        no_frames_to_track = 5
    elif performace == 2:
        scale_factor = 0.5
        tracking = True
        no_frames_to_track = 5
    elif performace == 3:
        scale_factor = 0.85
        tracking = True
        no_frames_to_track = 5
    if action == 2:
        #if selected access the overlay image
        overlay = cv.imread(overlay_location) 
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
            if n != no_frames_to_track and tracking == True:
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
                                new_frame = editing_image.blur(frame, target_face_location, used_kcf, 1)
                            elif action == 2:
                                new_frame = editing_image.replace(frame, overlay, target_face_location, used_kcf, 1)
            else:
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
                                    new_frame = editing_image.blur(frame, target_face_location, used_kcf, scale_factor)
                                elif action == 2:
                                    new_frame = editing_image.replace(frame, overlay, target_face_location, used_kcf, scale_factor)
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
                                        new_frame = editing_image.blur(frame, target_face_location, used_kcf, 1)
                                    elif action == 2:
                                        new_frame = editing_image.replace(frame, overlay, target_face_location, used_kcf, 1)
                else:
                    new_frame = frame
        

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