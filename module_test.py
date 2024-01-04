#import face_id_picture
import video

face_to_search_for_location = "/home/noah/Documents/software_mp/test data/img2.jpg"
images_to_search_location = "/home/noah/Documents/software_mp/test data/"

#results = face_id_picture.__init__(images_to_search_location, face_to_search_for_location, action_passed=1, overlay_location='')

#print(results)

video.video_cap(face_to_search_for_location, performace=2, action=1, overlay_location='')