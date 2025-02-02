import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QSlider, QLabel, QPushButton, 
    QWidget, QDesktopWidget, QFileDialog
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QMainWindow):
    def __init__(self, video_path, initial_opacity):
        super().__init__()
        self.setWindowTitle("Video Player")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.showFullScreen()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.playlist = QMediaPlaylist(self)
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.playlist.setCurrentIndex(0)
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop) 

        self.media_player.setPlaylist(self.playlist)

        video_widget = QVideoWidget()
        self.setCentralWidget(video_widget)
        self.media_player.setVideoOutput(video_widget)

        self.media_player.setVolume(50) 
        self.media_player.play()

        self.setWindowOpacity(initial_opacity)

    def close_video(self):
        self.media_player.stop()
        self.close()

    def closeEvent(self, event):
        self.media_player.stop()
        event.accept()


class ControlsOverlay(QWidget):
    def __init__(self, video_player, initial_opacity):
        super().__init__()
        self.video_player = video_player

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(screen_geometry.width() // 2 - 150, screen_geometry.height() - 150, 300, 150)

        layout = QVBoxLayout()

        self.pause_button = QPushButton("Pausa", self)
        self.pause_button.clicked.connect(self.toggle_pause)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(initial_opacity * 100))
        self.opacity_slider.valueChanged.connect(self.set_opacity)

        layout.addWidget(self.pause_button)
        layout.addWidget(QLabel("Volume"))
        layout.addWidget(self.volume_slider)
        layout.addWidget(QLabel("Opacità"))
        layout.addWidget(self.opacity_slider)

        self.setLayout(layout)
        self.setWindowOpacity(0.8)

        self.setVisible(False)

    def toggle_pause(self):
        if self.video_player.media_player.state() == QMediaPlayer.PlayingState:
            self.video_player.media_player.pause()
            self.pause_button.setText("Resume")
        else:
            self.video_player.media_player.play()
            self.pause_button.setText("Pause")

    def set_volume(self, value):
        self.video_player.media_player.setVolume(value)

    def set_opacity(self, value):
        self.video_player.setWindowOpacity(value / 100)


class ToggleButton(QWidget):
    def __init__(self, controls_overlay, video_player):
        super().__init__()
        self.controls_overlay = controls_overlay
        self.video_player = video_player

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(screen_geometry.width() - 100, screen_geometry.height() // 2 - 50, 50, 100)

        layout = QVBoxLayout()

        self.toggle_button = QPushButton("❌", self)
        self.toggle_button.clicked.connect(self.toggle_controls)

        self.close_button = QPushButton("Close video", self)
        self.close_button.clicked.connect(self.video_player.close_video)

        layout.addWidget(self.toggle_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.setWindowOpacity(0.5)

    def toggle_controls(self):
        if self.controls_overlay.isVisible():
            self.controls_overlay.hide()
            self.toggle_button.setText("⚙️")
        else:
            self.controls_overlay.show()
            self.toggle_button.setText("❌")


def select_video_file():
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(
        None,
        "Select Video File",
        "",
        "Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)"
    )
    return file_path


if __name__ == "__main__":
    app = QApplication(sys.argv)

    video_path = select_video_file()
    if not video_path:
        sys.exit(0)  

    initial_opacity = 0.3

    video_player = VideoPlayer(video_path, initial_opacity)
    video_player.show()

    controls_overlay = ControlsOverlay(video_player, initial_opacity)
    toggle_button = ToggleButton(controls_overlay, video_player)
    controls_overlay.show()
    toggle_button.show()

    sys.exit(app.exec_())
