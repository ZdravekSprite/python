from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyle, \
    QHBoxLayout, QVBoxLayout, QSlider, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys
import gpmf
import gpxpy
import ffmpeg


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle('PyQt5Player')
        self.setGeometry(350, 100, 800, 500)

        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        self.openBtn = QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)

        vbox = QVBoxLayout()

        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)

        self.mediaPlayer.setVideoOutput(videowidget)

        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.metaDataChanged.connect(self.metaData_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video')

        if filename != '':

            print(filename)
            # Read the binary stream from the file
            stream = gpmf.io.extract_gpmf_stream(filename)

            # Extract GPS low level data from the stream
            gps_blocks = gpmf.gps.extract_gps_blocks(stream)
            #print(gps_blocks)
            # Parse low level data into more usable format
            gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
            print(f"first timestamp {gps_data[0].timestamp}")
            #print(gps_data[0])
            print(f"last timestamp {gps_data[len(gps_data)-1].timestamp}")
            #print(gps_data[len(gps_data)-1])
            print(f"GPSData {len(gps_data)}")
            gpx = gpxpy.gpx.GPX()
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)
            gpx_track.segments.append(gpmf.gps.make_pgx_segment(gps_data))

            # print(gpx.to_xml())

            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            print(f"Now paused")
        else:
            self.mediaPlayer.play()
            timeStamp = self.mediaPlayer.metaData(
                QMediaMetaData.DateTimeOriginal)
            print(f"Now playing {timeStamp}")

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def metaData_changed(self):
        self.setWindowTitle('PyQt5Player1')

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        print(f"duration {duration}")

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
