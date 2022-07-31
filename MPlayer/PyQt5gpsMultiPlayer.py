from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyle, \
    QHBoxLayout, QVBoxLayout, QSlider, QFileDialog, QLabel, \
    QGraphicsView,  QGraphicsScene, QGraphicsProxyWidget

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from datetime import datetime
import sys
import gpmf
import gpxpy


class VideoSpec:
    def __init__(self, start=0, end=0, corection=0):
        self.start = start
        self.end = end
        self.corection = corection

class RotatableContainer(QGraphicsView):
    def __init__(self, widget: QWidget, rotation: float):
        super(QGraphicsView, self).__init__()

        scene = QGraphicsScene(self)
        self.setScene(scene)

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(widget)
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())
        self.proxy.setRotation(rotation)
        scene.addItem(self.proxy)

    def rotate(self, rotation: float):
        self.proxy.setRotation(rotation)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle('PyQt5MultiPlayer')
        self.setGeometry(100, 100, 1500, 490)

        self.create_player()

    def create_player(self):
        self.mediaPlayer1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget1 = QVideoWidget()
        container1 = RotatableContainer(widget=videoWidget1, rotation=0)
        videoWidget2 = QVideoWidget()
        container2 = RotatableContainer(widget=videoWidget2, rotation=0)

        self.v1 = VideoSpec()
        self.v2 = VideoSpec()

        self.openBtn1 = QPushButton('Open Video 1')
        self.openBtn1.clicked.connect(self.open_file1)
        self.rotationBtn1up = QPushButton('Rotate 1up')
        self.rotationBtn1up.clicked.connect(lambda: container1.rotate(0))
        self.rotationBtn1down = QPushButton('Rotate 1down')
        self.rotationBtn1down.clicked.connect(lambda: container1.rotate(180))

        self.openBtn2 = QPushButton('Open Video 2')
        self.openBtn2.clicked.connect(self.open_file2)
        self.rotationBtn2up = QPushButton('Rotate 2up')
        self.rotationBtn2up.clicked.connect(lambda: container2.rotate(0))
        self.rotationBtn2down = QPushButton('Rotate 2down')
        self.rotationBtn2down.clicked.connect(lambda: container2.rotate(180))

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

        #videoBox.addWidget(videoWidget1)
        videoBox.addWidget(container1)
        #videoBox.addWidget(videoWidget2)
        videoBox.addWidget(container2)

        self.labelStart1 = QLabel('start', self)
        self.labelStart1.setFixedHeight(15)
        self.labelStart1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelNow1 = QLabel('now', self)
        self.labelNow1.setFixedHeight(15)
        self.labelNow1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelEnd1 = QLabel('end', self)
        self.labelEnd1.setFixedHeight(15)
        self.labelEnd1.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.labelStart2 = QLabel('start', self)
        self.labelStart2.setFixedHeight(15)
        self.labelStart2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelNow2 = QLabel('now', self)
        self.labelNow2.setFixedHeight(15)
        self.labelNow2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelEnd2 = QLabel('end', self)
        self.labelEnd2.setFixedHeight(15)
        self.labelEnd2.setAlignment(Qt.AlignmentFlag.AlignRight)

        labelBox = QHBoxLayout()
        labelBox.setContentsMargins(0, 0, 0, 0)
        labelBox.addWidget(self.labelStart1)
        labelBox.addWidget(self.labelNow1)
        labelBox.addWidget(self.rotationBtn1up)
        labelBox.addWidget(self.rotationBtn1down)
        labelBox.addWidget(self.labelEnd1)
        labelBox.addWidget(self.labelStart2)
        labelBox.addWidget(self.labelNow2)
        labelBox.addWidget(self.rotationBtn2up)
        labelBox.addWidget(self.rotationBtn2down)
        labelBox.addWidget(self.labelEnd2)

        vbox = QVBoxLayout()

        vbox.addLayout(labelBox)
        vbox.addLayout(videoBox)
        vbox.addLayout(hbox)

        self.mediaPlayer1.setVideoOutput(videoWidget1)
        self.mediaPlayer2.setVideoOutput(videoWidget2)

        self.setLayout(vbox)

        self.mediaPlayer1.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer2.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer1.positionChanged.connect(self.position1_changed)
        self.mediaPlayer2.positionChanged.connect(self.position2_changed)
        self.mediaPlayer1.durationChanged.connect(self.duration_changed)
        self.mediaPlayer2.durationChanged.connect(self.duration_changed)

    def open_file1(self):
        self.mediaPlayer1.pause()
        self.mediaPlayer2.pause()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video 1')

        if filename != '':
            self.print_gps_data(filename, self.v1,
                                self.labelStart1, self.labelEnd1)
            self.mediaPlayer1.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn1.setEnabled(True)

    def open_file2(self):
        self.mediaPlayer1.pause()
        self.mediaPlayer2.pause()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video 2')

        if filename != '':
            self.print_gps_data(filename, self.v2,
                                self.labelStart2, self.labelEnd2)
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

    def position1_changed(self, position):
        if self.v1.start != 0:
            now1 = datetime.fromtimestamp(
                (self.v1.start + self.mediaPlayer1.position())/1000)
            now1_string = now1.strftime('%Y-%m-%d %H:%M:%S.%f')
            self.labelNow1.setText(now1_string[:-3])

        self.slider.setValue(position + self.v1.corection)

    def position2_changed(self, position):
        if self.v2.start != 0:
            now2 = datetime.fromtimestamp(
                (self.v2.start + self.mediaPlayer2.position())/1000)
            now2_string = now2.strftime('%Y-%m-%d %H:%M:%S.%f')
            self.labelNow2.setText(now2_string[:-3])

        self.slider.setValue(position + self.v2.corection)

    def duration_changed(self, duration):
        if self.v1.start >= self.v2.start and self.v2.start != 0:
            theStart = self.v2.start
        else:
            theStart = self.v1.start

        if self.v1.end > self.v2.end:
            theEnd = self.v1.end
        else:
            theEnd = self.v2.end

        if self.v1.start != 0 and self.v2.start == 0:
            print(f"v1.end {self.v1.end}")
            self.slider.setRange(0, self.mediaPlayer1.duration())
        if self.v1.start == 0 and self.v2.start != 0:
            print(f"v1.end {self.v2.end}")
            self.slider.setRange(0, self.mediaPlayer2.duration())
        if self.v1.start != 0 and self.v2.start != 0:
            print(f"theEnd-theStart {theEnd-theStart}")
            self.slider.setRange(0, theEnd-theStart)

        self.mediaPlayer1.setPosition(self.slider.sliderPosition() - self.v1.corection)
        self.mediaPlayer2.setPosition(self.slider.sliderPosition() - self.v2.corection)

    #    self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer1.setPosition(position - self.v1.corection)
        self.mediaPlayer2.setPosition(position - self.v2.corection)

    def print_gps_data(self, filename, video, labelStart, labelEnd):
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

        labelStart.setText(gps_data[0].timestamp)
        start = gps_data[0].timestamp
        dt_start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        video.start = int(dt_start.timestamp() * 1000)

        print(f"last timestamp {gps_data[len(gps_data)-1].timestamp}")
        # print(gps_data[len(gps_data)-1])

        labelEnd.setText(gps_data[len(gps_data)-1].timestamp)
        end = gps_data[len(gps_data)-1].timestamp
        dt_end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        video.end = int(dt_end.timestamp() * 1000)

        if self.v1.start != 0 and self.v2.start != 0:
            if self.v1.start > self.v2.start:
                self.v1.corection = self.v1.start - self.v2.start
                self.v2.corection = 0
            elif self.v1.start <= self.v2.start:
                self.v1.corection = 0
                self.v2.corection = self.v2.start - self.v1.start

        print(f"v1.corection {self.v1.corection}")
        print(f"v2.corection {self.v2.corection}")

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
