from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyle, \
    QHBoxLayout, QVBoxLayout, QSlider, QFileDialog, QLabel, \
    QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QRectF
from datetime import datetime
import sys
import gpmf
import gpxpy


class RotatableContainer(QGraphicsView):
    def __init__(self, widget: QWidget, rotation: float, width: float, height: float):
        super(QGraphicsView, self).__init__()

        scene = QGraphicsScene(self)
        self.setScene(scene)

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(widget)
        self.proxy.setTransformOriginPoint(self.proxy.boundingRect().center())
        self.proxy.setRotation(rotation)
        self.proxy.setGeometry(QRectF(0,0,width,height))
        scene.addItem(self.proxy)

    def rotate(self, rotation: float):
        self.proxy.setRotation(rotation)

    def size(self, width: float, height: float):
        self.proxy.setGeometry(QRectF(0,0,width,height))

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.setWindowTitle('PyQt5Player')
        self.setGeometry(350, 100, 750, 500)

        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()
        container = RotatableContainer(videoWidget, 0, 848, 480)

        self.openBtn = QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        self.rotationBtnUp = QPushButton('Rotate Up')
        self.rotationBtnUp.clicked.connect(lambda: container.rotate(0))

        self.rotationBtnDown = QPushButton('Rotate Down')
        self.rotationBtnDown.clicked.connect(lambda: container.rotate(180))

        self.sizeBtn = QPushButton('Resize')
        self.sizeBtn.clicked.connect(lambda: container.size(600,400))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)

        self.labelStart = QLabel('start',self)
        self.labelStart.setFixedHeight(15)
        self.labelStart.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelNow = QLabel('now',self)
        self.labelNow.setFixedHeight(15)
        self.labelNow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelEnd = QLabel('end',self)
        self.labelEnd.setFixedHeight(15)
        self.labelEnd.setAlignment(Qt.AlignmentFlag.AlignRight)

        labelBox = QHBoxLayout()
        labelBox.setContentsMargins(0, 0, 0, 0)
        labelBox.addWidget(self.labelStart)
        labelBox.addWidget(self.labelNow)
        labelBox.addWidget(self.rotationBtnUp)
        labelBox.addWidget(self.rotationBtnDown)
        labelBox.addWidget(self.sizeBtn)
        labelBox.addWidget(self.labelEnd)

        vbox = QVBoxLayout()

        vbox.addLayout(labelBox)
        vbox.addWidget(container)
        vbox.addLayout(hbox)

        self.mediaPlayer.setVideoOutput(videoWidget)

        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.metaDataChanged.connect(self.metaData_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video')

        if filename != '':
            self.print_gps_data(filename)
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
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.setWindowTitle(dt_string)

    def position_changed(self, position):
        start = self.labelStart.text()
        dt_obj = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        millisec = int(dt_obj.timestamp() * 1000)
        now = datetime.fromtimestamp((millisec + position)/1000)
        now_string = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        self.labelNow.setText(now_string[:-3])
        # self.labelNow.setText(str(position))
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        print(f"duration {duration}")

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

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
        self.labelStart.setText(gps_data[0].timestamp)
        print(f"last timestamp {gps_data[len(gps_data)-1].timestamp}")
        # print(gps_data[len(gps_data)-1])
        self.labelEnd.setText(gps_data[len(gps_data)-1].timestamp)
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
