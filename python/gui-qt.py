import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton, QPushButton, QLabel, QGridLayout, QListWidget, QMessageBox
from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
import re
import cv2 as cv
import os
import editing_image
from face_id_picture import get_files
from time import sleep
from multiprocessing import cpu_count, Queue, Pool, Value
import face_recognition
from threading import Thread

target_face_location = ""
images_to_search_location = ""
overlay_image_location = ""
action = 0
progress = Value('i', 0)


class Window(QDialog):
    # Logic for getting radio button value
    @Slot()
    def radio(self):
        global action
        button = self.sender()
        action = button.option


    # For end screen
    def end_screen(self, results):
        self.close()
        end_grid = QGridLayout()
        for image_name in results:
            #image_name = image_name + ".temp"
            image = cv.imread(image_name)
            # Get the dimensions of the image (height, width, number_of_channels)
            height, width, channels = image.shape
            scale_factor = 200/height
            new_width = int(round(scale_factor*width, 0))
            resized_image = cv.resize(image, (new_width, 200), interpolation=cv.INTER_AREA)
            imgbytes = cv.imencode(".png", resized_image)[1].tobytes()
            image_display =  QLabel(self)
            pixmap = QPixmap(resized_image)
            image_display.setPixmap(pixmap)
            end_grid.addWidget(image_display, 0,0)


    # Logic for progress bar
    def progress_bar_update(self, images_to_search):
        percentage = 0
        while percentage <= 100:
            percentage = progress.value * (100/len(images_to_search))
            self.progress_bar.setValue(percentage)
            sleep(0.5)

    # For standard buttons
    @Slot()
    def accept(self):
        images_to_search = get_files(images_to_search_location)
        if images_to_search_location != '' and action != 0 and target_face_location != '' and images_to_search != []:
            # Call function to get files in directory
            processing_thread = Thread(target=start, args=[images_to_search, action])
            processing_thread.start()
            progress_thread = Thread(target=Window.progress_bar_update, args=[self, images_to_search])
            progress_thread.start()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Enter required information")
            msgBox.exec()


    @Slot()
    def cancel(self):
        self.close()

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Face removal tool")
        dialogLayout = QVBoxLayout()
        #formLayout = QFormLayout()
        gridLayout = QGridLayout()
        # Selecting target face image
        target_image_button = QPushButton("Browse")
        self.target_image_text_box = QLineEdit()
        gridLayout.addWidget(QLabel("Select the image containing the face to search for:"), 0, 0)
        gridLayout.addWidget(self.target_image_text_box, 0, 1)
        gridLayout.addWidget(target_image_button, 0, 2)
        target_image_button.clicked.connect(self.select_target_face)
        #Selecting image directory
        select_image_directory_button = QPushButton("Browse")
        self.select_image_directory_text_box = QLineEdit()
        gridLayout.addWidget(QLabel("Select the directory contining images to search:"), 1, 0)
        gridLayout.addWidget(self.select_image_directory_text_box, 1, 1)
        gridLayout.addWidget(select_image_directory_button, 1, 2)
        select_image_directory_button.clicked.connect(self.select_image_directory)

        # List images
        self.image_list_box = QListWidget()
        gridLayout.addWidget(self.image_list_box, 2, 0, 1, 2)

        # Select action option
        blur_button = QRadioButton("Blur matching faces", self)
        blur_button.option = 1
        replace_button = QRadioButton("Replace matching faces", self)
        replace_button.option = 2
        delete_button = QRadioButton("Delete images containg matching faces", self)
        delete_button.option = 3
        # Add radio buttons to layout
        gridLayout.addWidget(QLabel("What should the program do to matching faces:"), 3, 0, 1, 2)
        gridLayout.addWidget(blur_button, 4, 0)
        gridLayout.addWidget(replace_button, 5, 0)
        gridLayout.addWidget(delete_button, 6, 0)
        # Connect radio buttons to fuction
        blur_button.clicked.connect(self.radio)
        replace_button.clicked.connect(self.radio)
        delete_button.clicked.connect(self.radio)


        # Select overlay image if applicable
        select_overlay_button = QPushButton("Browse")
        self.select_overlay_text_box = QLineEdit()
        gridLayout.addWidget(QLabel("Select the overlay image:"), 7, 0)
        gridLayout.addWidget(self.select_overlay_text_box, 7, 1)
        gridLayout.addWidget(select_overlay_button, 7, 2)
        select_overlay_button.clicked.connect(self.select_overlay_image)


        # Add formLayout to dialogLayout
        dialogLayout.addLayout(gridLayout)

        # Progress bar
        self.progress_bar = QProgressBar()
        dialogLayout.addWidget(self.progress_bar)


        # Add standard buttons
        self.standard_buttons = QDialogButtonBox(QDialogButtonBox.Ok

                             | QDialogButtonBox.Cancel)
        dialogLayout.addWidget(self.standard_buttons)
        # Connect the accepted and rejected signals to respective methods
        self.standard_buttons.accepted.connect(self.accept)
        self.standard_buttons.rejected.connect(self.reject)


        # Set dialogLayout to be the layout of the window
        self.setLayout(dialogLayout)

    # Logic for selecting overlay image
    @Slot()
    def select_overlay_image(self):
        global overlay_image_location
        overlay_image_location_untrimmed = QFileDialog.getOpenFileName(self, ("Open image"), "", ("folder (*.png *.jpg *.bmp)"))
        if overlay_image_location_untrimmed:
            self.select_overlay_text_box.clear()
            # Use regular expression to find the file path
            overlay_image_location = re.search(r"'(.*?)'", str(overlay_image_location_untrimmed)).group(1)
            self.select_overlay_text_box.setText(overlay_image_location)

    # Logic for selecting image directory
    @Slot()
    def select_image_directory(self):
        global images_to_search_location
        images_to_search_location = QFileDialog.getExistingDirectory(self, ("Open folder"))
        if images_to_search_location:
            self.select_image_directory_text_box.clear()
            self.select_image_directory_text_box.setText(str(images_to_search_location))
            # Display images in directory
            try:
                # Get list of files in folder
                file_list = os.listdir(images_to_search_location)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(images_to_search_location, f))
                and f.lower().endswith((".png", ".gif", '.jpg'))
            ]
            for image in fnames:
                self.image_list_box.addItem(image)


    # Logic for selecting target image
    @Slot()
    def select_target_face(self):
        global target_face_location
        target_face_location_untrimmed = QFileDialog.getOpenFileName(self, ("Open image"), "", ("folder (*.png *.jpg *.bmp)"))
        if target_face_location_untrimmed:
            self.target_image_text_box.clear()
            # Use regular expression to find the file path
            target_face_location = re.search(r"'(.*?)'", str(target_face_location_untrimmed)).group(1)
            self.target_image_text_box.setText(target_face_location)



    # Display selected target image
    def display_target_image(self):
        pass


def start(images_to_search, action):
    global face_to_search_for_encoding, overlay
    progress.value = 0
    # Process the image contaning the face to search for
    try:
        face_to_search_for = face_recognition.load_image_file(target_face_location)
        face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]
    except:
        msgBox = QMessageBox()
        msgBox.setText("No face found in image containing target face")
        msgBox.exec()
    if action == 2:
        #if selected access the overlay image
        overlay = cv.imread(overlay_image_location)
    with Pool(processes=cpu_count()) as pool:
        # Map the image processing function over the images
        results = pool.map(face_recog, images_to_search)
    results = [item for item in results if item is not None]
    msgBox = QMessageBox()
    msgBox.setText("The images have been searched")
    msgBox.exec()
    Window.show_end_screen(results=results)



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
                face_locations = face_recognition.face_locations(image)
                for face_location in face_locations:
                    # See if the face is a match for the known face
                    face_encoding = face_recognition.face_encodings(image, [face_location])[0]
                    match = face_recognition.compare_faces([face_to_search_for_encoding], face_encoding)
                    # If it's a match, blur the face
                    if match[0]:
                        if action == 1:
                            new_image = editing_image.blur(image_bgr, target_face_location, False, 1)
                        elif action == 2:
                            new_image = editing_image.replace(image_bgr, overlay, target_face_location, False, 1)
                        #cv.imwrite(image_name, new_image)
                        progress.value += 1
                    return image_name

            else:
                # Put progress update to the queue
                progress.value += 1
                return f"Image {image_name} doesn't match"
        else:
            # Put progress update to the queue
            progress.value += 1
            return f"No faces found in image {image_name}"

    except Exception as e:
        progress.value += 1
        return f"An error occurred with image {image_name}: {e}"


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
