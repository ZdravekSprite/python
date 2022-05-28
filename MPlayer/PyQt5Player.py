from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyle, \
    QHBoxLayout, QVBoxLayout, QSlider, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle('PyQt5Player')

        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        self.openBtn = QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)

        vbox = QVBoxLayout()

        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video')

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
