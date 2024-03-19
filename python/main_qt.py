import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton, QPushButton, QLabel, QGridLayout, QListWidget, QMessageBox
from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
import re
import cv2 as cv
import os
from time import sleep
from multiprocessing import cpu_count, Queue, Pool, Value, Process, Event, freeze_support
import pathlib
import face_recognition
import concurrent.futures

progress = Value('i', 0)
images_to_search = []
event = Event()
data_queue = Queue()

class Window(QDialog):
    # Logic for getting radio button value
    @Slot()
    def radio(self):
        button = self.sender()
        self.action = button.option

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
    # Logic for selecting target image
    @Slot()
    def select_target_face(self):
        target_face_location_untrimmed = QFileDialog.getOpenFileName(self, ("Open image"), "", ("Image (*.png *.jpg *.bmp)"))
        if target_face_location_untrimmed:
            self.target_image_text_box.clear()
            # Use regular expression to find the file path
            # THIS STRING PROCESSING IS A STARDARD ALGORITHM
            self.target_face_location = re.search(r"'(.*?)'", str(target_face_location_untrimmed)).group(1)
            self.target_image_text_box.setText(self.target_face_location)

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
        # Input checking
        if self.images_to_search_location != '' and self.action != 0 and self.target_face_location != '':
            # Setup worker to update progress bar
            progress_worker = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            progress_worker.submit(self.progress_bar_update, self.images_to_search)
            #images_to_search = get_files(self.images_to_search_location)
            # Use of queues to transfer data from frontend to backend
            data_queue.put([self.action, self.target_face_location, self.images_to_search, self.overlay_image_location])
            # Tell the backend to run
            event.set()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Enter required information")
            msgBox.exec()


    @Slot()
    def cancel(self):
        self.close()

    def __init__(self):
        # Set overlay_image_location to none in case it's not applicable
        self.overlay_image_location = None
        super().__init__(parent=None)
        self.setWindowTitle("Face removal tool v0.8")
        dialogLayout = QVBoxLayout()
        #formLayout = QFormLayout()
        gridLayout = QGridLayout()
        # Selecting target face image
        target_image_button = QPushButton("Browse")
        self.target_image_text_box = QLineEdit()
        self.target_image_text_box.setReadOnly(True)
        gridLayout.addWidget(QLabel("Select the image containing the face to search for:"), 0, 0)
        gridLayout.addWidget(self.target_image_text_box, 0, 1)
        gridLayout.addWidget(target_image_button, 0, 2)
        target_image_button.clicked.connect(self.select_target_face)
        #Selecting image directory
        select_image_directory_button = QPushButton("Browse")
        self.select_image_directory_text_box = QLineEdit()
        self.select_image_directory_text_box.setReadOnly(True)
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
        self.select_overlay_text_box.setReadOnly(True)
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
        overlay_image_location_untrimmed = QFileDialog.getOpenFileName(self, ("Open image"), "", ("Image (*.png *.jpg *.bmp)"))
        if overlay_image_location_untrimmed:
            self.select_overlay_text_box.clear()
            # Use regular expression to find the file path
            self.overlay_image_location = re.search(r"'(.*?)'", str(overlay_image_location_untrimmed)).group(1)
            self.select_overlay_text_box.setText(overlay_image_location)

    # Logic for selecting image directory
    @Slot()
    def select_image_directory(self):
        self.images_to_search_location = QFileDialog.getExistingDirectory(self, ("Open folder"))
        if self.images_to_search_location:
            self.select_image_directory_text_box.clear()
            self.select_image_directory_text_box.setText(str(self.images_to_search_location))
            # Display images in directory
            self.images_to_search = get_files(self.images_to_search_location)
            for image in images_to_search:
                self.image_list_box.addItem(image)


class backend:

    def __init__(self):
        # Create backend windows for popups
        app = QApplication([])
        window = Window()
        # Wait for trigger
        event.wait()
        # Get input data
        input_data = data_queue.get()
        self.action = input_data[0]
        self.target_face_location = input_data[1]
        self.images_to_search = input_data[2]
        self.overlay_image_location = input_data[3]
        # Call function to spawn processing threads
        self.start(self.images_to_search, self.action)

    def start(self, images_to_search, action):
        progress.value = 0
        # Process the image contaning the face to search for
        try:
            face_to_search_for = face_recognition.load_image_file(self.target_face_location)
            self.face_to_search_for_encoding = face_recognition.face_encodings(face_to_search_for)[0]
        except Exception as e:
            print(f"Error {e}")
            msgBox = QMessageBox()
            msgBox.setText(f"No face found in image containing target face\n{e}")
            msgBox.exec()
        if action == 2:
            #if selected access the overlay image
            self.overlay = cv.imread(self.overlay_image_location)
        with Pool(processes=cpu_count()) as pool:
            # Map the image processing function over the images
            results = pool.map(self.face_recog, images_to_search)
        results = [item for item in results if item is not None]
        msgBox = QMessageBox()
        msgBox.setText("The images have been searched")
        msgBox.exec()
        #Window.show_end_screen(results=results)



    def face_recog(self, image_name):
        try:
            # Load and run face recognition on the image to search
            image = face_recognition.load_image_file(image_name)
            image_encodings = face_recognition.face_encodings(image)
            if image_encodings:
                image_encoding = image_encodings[0]
                # Compare faces
                results = face_recognition.compare_faces([self.face_to_search_for_encoding], image_encoding)
                # Convert image to BGR for OpenCV
                image_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                if results[0]:
                    # Get location of faces in image
                    face_locations = face_recognition.face_locations(image)
                    for face_location in face_locations:
                        # See if the face is a match for the known face
                        face_encoding = face_recognition.face_encodings(image, [face_location])[0]
                        match = face_recognition.compare_faces([self.face_to_search_for_encoding], face_encoding)
                        # If it's a match, blur the face
                        if match[0]:
                            if self.action == 1:
                                # Call editing image class blur function
                                new_image = editing_image.blur(image_bgr, face_location, 1)
                            elif self.action == 2:
                                new_image = editing_image.replace(image_bgr, self.overlay, face_location, 1)
                            elif self.action == 3:
                                os.remove(image_name)
                            cv.imwrite(image_name, new_image)
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


def get_files(images_to_search_location):
    global images_to_search
    for file in pathlib.Path(images_to_search_location).rglob("*.jpg"):
        images_to_search.append(str(file))
    for file in pathlib.Path(images_to_search_location).rglob("*.JPG"):
        images_to_search.append(str(file))
    for file in pathlib.Path(images_to_search_location).rglob("*.png"):
        images_to_search.append(str(file))
    return list(images_to_search)

class editing_image():
    #EDITING IMAGES

    def blur(image_bgr, target_face_location, scale_factor):
        # Unpack the location
        top, right, bottom, left = target_face_location
        # Scale face_location coordinates up to the original image size
        top = int(top / scale_factor)
        right = int(right / scale_factor)
        bottom = int(bottom / scale_factor)
        left = int(left / scale_factor)
        # Calculate the width and height of the bounding box
        width = right - left
        height = bottom - top
        # Increase the region slightly to make sure the entire face is covered
        top = max(top - 10, 0)
        right = min(right + 10, image_bgr.shape[1])
        bottom = min(bottom + 10, image_bgr.shape[0])
        left = max(left - 10, 0)

        # Select the region of interest (ROI) where the face is located
        face_roi = image_bgr[top:bottom, left:right]

        # Apply a Gaussian blur to the face region
        blurred_face = cv.GaussianBlur(face_roi, (999, 999), 0)

        # Replace the original image region with the blurred face
        image_bgr[top:bottom, left:right] = blurred_face

        return image_bgr

    def replace(background, overlay, target_face_location, scale_factor):
        # Unpack the location
        top, right, bottom, left = target_face_location
        # Scale face_location coordinates up to the original image size
        top = int(top / scale_factor)
        right = int(right / scale_factor)
        bottom = int(bottom / scale_factor)
        left = int(left / scale_factor)
        # Calculate the width and height of the bounding box
        width = right - left
        height = botton - top
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




def ui_start():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

def main():
    # For pyinstaller
    freeze_support()
    # creating processes
    frontend_thread = Process(target=ui_start)
    backend_thread = Process(target=backend)
    frontend_thread.start()
    backend_thread.start()
    frontend_thread.join()
    backend_thread.join()

if __name__ == "__main__":
    main()
