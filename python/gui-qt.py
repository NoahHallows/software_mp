import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton, QPushButton, QLabel, QGridLayout
from PySide6.QtCore import Slot

class Window(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Face removal tool")
        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()
        gridLayout = QGridLayout()
        # Selecting target face image
        select_image_button = QPushButton("Browse")
        self.select_image_text_box = QLineEdit()
        gridLayout.addWidget(QLabel("Select the image containing the face to search for:"), 0, 0)
        gridLayout.addWidget(self.select_image_text_box, 0, 1)
        gridLayout.addWidget(select_image_button, 0, 2)
        select_image_button.clicked.connect(self.select_target_face)
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
        images_to_search_location = QFileDialog.getOpenFileName(self, ("Open folder"), "", ("folder (*.png *.jpg *.bmp)"))
        if images_to_search_location:
            self.select_image_directory_text_box.clear()
            self.select_image_directory_text_box.setText(str(images_to_search_location))
    # Logic for selecting target image
    @Slot()
    def select_target_face(self):
        target_face_location = QFileDialog.getOpenFileName(self, ("Open folder"), "", ("folder (*.png *.jpg *.bmp)"))
        if target_face_location:
            self.update(QLabel(f"Selected image {target_face_location}"))



if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
