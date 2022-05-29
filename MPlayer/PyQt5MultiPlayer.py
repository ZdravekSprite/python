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
        self.setGeometry(100, 100, 1000, 500)

        self.create_player()

    def create_player(self):
        self.mediaPlayer1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget1 = QVideoWidget()
        videoWidget2 = QVideoWidget()

        self.openBtn1 = QPushButton('Open Video 1')
        self.openBtn1.clicked.connect(self.open_file1)

        self.openBtn2 = QPushButton('Open Video 2')
        self.openBtn2.clicked.connect(self.open_file2)

        self.playBtn1 = QPushButton()
        self.playBtn1.setEnabled(False)
        self.playBtn1.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn1.clicked.connect(self.play_video1)

        self.playBtn2 = QPushButton()
        self.playBtn2.setEnabled(False)
        self.playBtn2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn2.clicked.connect(self.play_video2)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openBtn1)
        hbox.addWidget(self.playBtn1)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.playBtn2)
        hbox.addWidget(self.openBtn2)

        videoBox = QHBoxLayout()

        videoBox.addWidget(videoWidget1)
        videoBox.addWidget(videoWidget2)

        vbox = QVBoxLayout()

        vbox.addLayout(videoBox)
        vbox.addLayout(hbox)

        self.mediaPlayer1.setVideoOutput(videoWidget1)
        self.mediaPlayer2.setVideoOutput(videoWidget2)

        self.setLayout(vbox)

        self.mediaPlayer1.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer1.positionChanged.connect(self.position_changed)
        self.mediaPlayer1.durationChanged.connect(self.duration_changed)

    def open_file1(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video 1')

        if filename != '':
            self.mediaPlayer1.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn1.setEnabled(True)

    def open_file2(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video 2')

        if filename != '':
            self.mediaPlayer2.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn2.setEnabled(True)

    def play_video1(self):
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer1.pause()
        else:
            self.mediaPlayer1.play()

    def play_video2(self):
        if self.mediaPlayer2.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer2.pause()
        else:
            self.mediaPlayer2.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
            self.playBtn1.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn1.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
        if self.mediaPlayer2.state() == QMediaPlayer.PlayingState:
            self.playBtn2.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn2.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))


    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer1.setPosition(position)
        self.mediaPlayer2.setPosition(position)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
