from PyQt6.QtWidgets import QApplication, QWidget, QStyle
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay))
        self.setWindowTitle('PyQt6Player')
        self.setGeometry(350, 100, 700, 500)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
