import sys
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QFileDialog, QProgressBar

class Window(QDialog):
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
        dialogLayout.addLayout(formLayout)
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