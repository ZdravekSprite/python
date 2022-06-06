from PyQt6.QtWidgets import QApplication, QWidget, QStyle, QPushButton, QSlider, \
    QHBoxLayout, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QRectF
import sys

class RotatableContainer(QGraphicsView):
    def __init__(self, widget: QWidget):
        super(QGraphicsView, self).__init__()

        scene = QGraphicsScene(self)
        self.setScene(scene)

        self.proxy = QGraphicsProxyWidget()
        self.proxy.setWidget(widget)
        scene.addItem(self.proxy)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay))
        self.setWindowTitle('PyQt6Player')

        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer()
        videoWidget = QVideoWidget()
        container = RotatableContainer(videoWidget)

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
        vbox.addWidget(container)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.mediaPlayer.setVideoOutput(videoWidget)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
