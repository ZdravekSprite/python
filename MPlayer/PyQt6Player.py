from PyQt6.QtWidgets import QApplication, QWidget, QStyle, QPushButton, QSlider, \
     QHBoxLayout, QVBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import Qt
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay))
        self.setWindowTitle('PyQt6Player')
        self.setGeometry(350, 100, 700, 500)

        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer()

        self.openBtn = QPushButton('Open Video')

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay))

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
