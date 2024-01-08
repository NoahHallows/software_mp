import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar, QRadioButton
from PySide6.QtCore import Slot

class Window(QDialog):
    @Slot()
    def checker(self):
        button = self.sender()
        print(f"option {button.option} was")
    
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QDialog")
        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()
        formLayout.addRow("Name:", QLineEdit())
        formLayout.addRow("Age:", QLineEdit())
        formLayout.addRow("Job:", QLineEdit())
        formLayout.addRow("Hobbies:", QLineEdit())
        formLayout.addRow("Progress", QProgressBar(value=50))
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
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        dialogLayout.addWidget(buttons)
        self.setLayout(dialogLayout)
    

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())