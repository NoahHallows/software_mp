import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton, QPushButton, QLabel, QGridLayout
from PySide6.QtCore import Slot
import re

class Window(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Face removal tool")
        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()
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
        
        # Add formLayout to dialogLayout
        dialogLayout.addLayout(gridLayout)
        # Set dialogLayout to be the layout of the window
        self.setLayout(dialogLayout)
    
    # Logic for selecting image directory
    @Slot()
    def select_image_directory(self):
        images_to_search_location = QFileDialog.getExistingDirectory(self, ("Open folder"))
        if images_to_search_location:
            self.select_image_directory_text_box.clear()
            self.select_image_directory_text_box.setText(str(images_to_search_location))  #('/home/noah/Documents/software_mp/test data/picture_of_me_at_mdda.jpg', 'folder (*.png *.jpg *.bmp)')
    # Logic for selecting target image
    @Slot()
    def select_target_face(self):
        target_face_location_untrimmed = QFileDialog.getOpenFileName(self, ("Open image"), "", ("folder (*.png *.jpg *.bmp)"))
        if target_face_location_untrimmed:
            self.target_image_text_box.clear()
            # Use regular expression to find the file path
            target_face_location = re.search(r"'(.*?)'", str(target_face_location_untrimmed)).group(1)
            self.target_image_text_box.setText(target_face_location)



if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
