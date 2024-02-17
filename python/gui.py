import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton
from PySide6.QtCore import Slot
from time import sleep
from threading import Thread
from multiprocessing import Pool

example_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

class Window(QDialog):
    @Slot()
    def checker(self):
        button = self.sender()
        print(f"option {button.option} was")

    @Slot()
    def accept(self):
        print("Ok button was clicked")
        #self.image_processor = self.update_progress_bar()
        #self.image_processor.run()
        t = Thread(target=Window.update_progress_bar, args=[self])
        t.start()
        t1 = Thread(target=start)
        t1.start()

        
    def update_progress_bar(self):
        for n in range(1, 101):
            self.progress_bar.setValue(n)
            print(n)
            sleep(0.5)
        
    
    @Slot()
    def cancel(self):
        print("Cancel button was clicked")
        self.close()
    
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QDialog")
        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()
        formLayout.addRow("Name:", QLineEdit())
        formLayout.addRow("Age:", QLineEdit())
        formLayout.addRow("Job:", QLineEdit())
        formLayout.addRow("Hobbies:", QLineEdit())
        self.progress_bar = QProgressBar(value=0)
        formLayout.addRow("Progress", self.progress_bar)
        button = QRadioButton("Button 1", self)
        button.option = 1
        button2 = QRadioButton("Button 2", self)
        button2.option = 2
        button3 = QRadioButton("Button 3", self)
        button3.option = 3
        dialogLayout.addLayout(formLayout)
        dialogLayout.addWidget(button)
        dialogLayout.addWidget(button2)
        dialogLayout.addWidget(button3)
        button.clicked.connect(self.checker)
        button2.clicked.connect(self.checker)
        button3.clicked.connect(self.checker)

        #fileName = QFileDialog.getOpenFileName(self, ("Open Image"), "/home/noah", ("Image Files (*.png *.jpg *.bmp)"))
        #print(fileName)
        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        dialogLayout.addWidget(self.buttons)
        self.setLayout(dialogLayout)
        
def example(array):
    sleep(5)
    print(array)

def start():
    with Pool(processes=10) as pool:
        # Map the image processing function over the images
        pool.map(example, example_array)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())