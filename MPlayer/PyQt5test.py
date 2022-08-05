import os
from turtle import width
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets

__appname__ = 'PyQt5'
__width__ = 848
__height__ = 480

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.setMinimumSize(QtCore.QSize(__width__, __height__+40))
        self._scene = QtWidgets.QGraphicsScene(self)
        self._gv = QtWidgets.QGraphicsView(self._scene)

        self._videoitem = QtMultimediaWidgets.QGraphicsVideoItem()
        self._videoitem.setSize(QtCore.QSizeF(__width__,__height__))
        self._scene.addItem(self._videoitem)
        
        self._player = QtMultimedia.QMediaPlayer(
            self, QtMultimedia.QMediaPlayer.VideoSurface
        )
        self._player.stateChanged.connect(self.on_stateChanged)
        self._player.setVideoOutput(self._videoitem)

        self.openBtn = QtWidgets.QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QtWidgets.QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.rotationBtn = QtWidgets.QPushButton('Rotate')
        self.rotationBtn.clicked.connect(self.rotate)
        self.rotationBtn.setEnabled(False)

        hbox = QtWidgets.QHBoxLayout()

        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.rotationBtn)

        vbox = QtWidgets.QVBoxLayout()

        vbox.addWidget(self._gv)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    @QtCore.pyqtSlot(QtMultimedia.QMediaPlayer.State)
    def on_stateChanged(self, state):
        if state == QtMultimedia.QMediaPlayer.PlayingState:
            self._gv.fitInView(self._videoitem, QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._gv.fitInView(self._videoitem, QtCore.Qt.KeepAspectRatio)

    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Video')

        if filename != '':
            self._player.setMedia(
                QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.rotationBtn.setEnabled(True)

    def play_video(self):
        if self._player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self._player.pause()
        else:
            self._player.play()

    def rotate(self):
        if self._videoitem.rotation():
            self._videoitem.setRotation(0)
            self._scene.setSceneRect(0, 0, __width__, __height__)
        else:
            self._videoitem.setRotation(180)
            self._scene.setSceneRect(-__width__, -__height__, __width__, __height__)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())