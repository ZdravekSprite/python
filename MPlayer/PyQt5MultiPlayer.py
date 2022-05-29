from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyle, \
    QHBoxLayout, QVBoxLayout, QSlider, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys
import gpmf
import gpxpy


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle('PyQt5MultiPlayer')
        self.setGeometry(100, 100, 1450, 450)

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
        self.playBtn1.clicked.connect(self.play_video)

        self.playBtn2 = QPushButton()
        self.playBtn2.setEnabled(False)
        self.playBtn2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn2.clicked.connect(self.play_video)

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
        self.mediaPlayer2.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer1.positionChanged.connect(self.position_changed)
        self.mediaPlayer1.durationChanged.connect(self.duration_changed)

    def open_file1(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video 1')

        if filename != '':
            self.print_gps_data(filename)
            self.mediaPlayer1.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn1.setEnabled(True)

    def open_file2(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video 2')

        if filename != '':
            self.print_gps_data(filename)
            self.mediaPlayer2.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn2.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer1.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer1.pause()
        else:
            self.mediaPlayer1.play()
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

    def print_gps_data(self, filename):
        print(filename)
        # Read the binary stream from the file
        stream = gpmf.io.extract_gpmf_stream(filename)
        # Extract GPS low level data from the stream
        gps_blocks = gpmf.gps.extract_gps_blocks(stream)
        # print(gps_blocks)
        # Parse low level data into more usable format
        gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
        print(f"first timestamp {gps_data[0].timestamp}")
        # print(gps_data[0])
        print(f"last timestamp {gps_data[len(gps_data)-1].timestamp}")
        # print(gps_data[len(gps_data)-1])
        print(f"GPSData {len(gps_data)}")
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(gpmf.gps.make_pgx_segment(gps_data))
        # print(gpx.to_xml())


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
