import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton, QPushButton, QLabel, QGridLayout, QListWidget
from PySide6.QtCore import Slot
import re
import cv2 as cv
import os
from face_id_picture import get_files

class Window(QDialog):
    target_face_location = ""
    images_to_search_location = ""
    overlay_image_location = ""
    action = 1
    # Logic for getting radio button value
    @Slot()
    def radio(self):
        global action
        button = self.sender()
        action = button.option  

    # For end screen
    def end_screen(self, results):
        end_grid = QGridLayout()
        x = 0
        y = 0
        for image_name in results:
            image_name = "." + image_name + ".temp"
            image = cv.imread(image_name)
            # Get the dimensions of the image (height, width, number_of_channels)
            height, width, channels = image.shape
            scale_factor = 200/height
            new_width = int(round(scale_factor*width, 0))
            resized_image = cv.resize(image, (new_width, 200), interpolation=cv.INTER_AREA)
            imgbytes = cv.imencode(".png", resized_image)[1].tobytes()
            image_display =  


    # For standard buttons
    @Slot()
    def accept(self):
        print("Ok button was clicked.")
        import face_id_picture
        results = face_id_picture.start_face_recognition(target_face_location, action, overlay_image_location)
        print(results)
        self.close()
        end_screen(self, results)
        

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
            self.select_image_directory_text_box.setText(str(images_to_search_location))  #('/home/noah/Documents/software_mp/test data/picture_of_me_at_mdda.jpg', 'folder (*.png *.jpg *.bmp)')
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
            # Call function to get files in directory
            get_files(images_to_search_location)

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







if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
