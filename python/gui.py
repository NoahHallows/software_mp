import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton
from PySide6.QtCore import Slot
from time import sleep

class Window(QDialog):
    @Slot()
    def checker(self):
        button = self.sender()
        print(f"option {button.option} was")
        self.close()

    @Slot()
    def accept(self):
        print("Ok button was clicked")
        
    
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
        progress_bar = QProgressBar(value=0)
        formLayout.addRow("Progress", progress_bar)
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

        fileName = QFileDialog.getOpenFileName(self, ("Open Image"), "/home/noah", ("Image Files (*.png *.jpg *.bmp)"))
        print(fileName)
        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        self.buttons.accepted.connect(self.accept)
        #self.buttons.rejected.connect(self.reject)
        dialogLayout.addWidget(self.buttons)
        self.setLayout(dialogLayout)
        n = 0
        while True:
            n = n + 1
            progress_bar.setValue(n)
            sleep(0.5)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())