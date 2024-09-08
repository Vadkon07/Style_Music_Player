import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QListWidget, QLabel, QFileDialog, QDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QColor
from pygame import mixer

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.IsPaused = False

        self.setWindowTitle('Style Player')
        self.setGeometry(100, 100, 480, 250)
        self.setStyleSheet('background-color: #000000; color: lime')
        self.setFixedSize(480, 250)

        mixer.init()
        layout = QVBoxLayout()

        self.lbl = QLabel(self)
        layout.addWidget(self.lbl)

        self.playlist = QListWidget(self)
        self.playlist.setStyleSheet('background-color: #000000; color: #00ff00; font: bold 12px;')
        layout.addWidget(self.playlist)

        self.play_button = QPushButton('Play', self)
        self.play_button.setStyleSheet("""
        QPushButton {
            border: 1px solid;
            border-color: lime; 
            margin: 1px;
            height: 25px;
            width: 25px;
        }
        QPushButton:focus {
            margin: 0px;
        }
        """)

        self.play_button.clicked.connect(self.play_music)
        layout.addWidget(self.play_button)

        self.toggle_button = QPushButton('Pause/Unpause', self)
        self.toggle_button.setStyleSheet("""
        QPushButton {
            border: 1px solid;
            border-color: lime; 
            margin: 1px;
            height: 25px;
            width: 25px;
        }
        QPushButton:focus {
            margin: 0px;
        }
        """)
        self.toggle_button.clicked.connect(self.toggleMusic)
        layout.addWidget(self.toggle_button)

        self.add_button = QPushButton('Add directory', self)
        self.add_button.setStyleSheet("""
        QPushButton {
            border: 1px solid;
            border-color: lime; 
            margin: 1px;
            height: 25px;
            width: 25px;
        }
        QPushButton:focus {
            margin: 0px;
        }
        """)
        self.add_button.clicked.connect(self.add_music)
        layout.addWidget(self.add_button)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: green;
            }
            QSlider::handle:horizontal {
                background: lime;
                border: 1px solid #999999;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)

        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.sliderMoved.connect(self.set_position)  

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider)
        self.timer.start(1000)

        self.is_slider_moving = False

    def exit_app(self):
        self.close()

    def toggleMusic(self):
        if self.IsPaused:
            mixer.music.unpause()
            self.IsPaused = False
        else:
            mixer.music.pause()
            self.IsPaused = True

    def update(self, ind):
        frame = self.frms[ind]
        ind += 1
        if ind == self.frmcount:
            ind = 0
        self.lbl.setPixmap(QPixmap(frame))
        QTimer.singleShot(40, lambda: self.update(ind))

    def add_music(self):
        dialog = QFileDialog(self)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setStyleSheet("""
            QDialog {
                background-color: black;
                color: lime;
            }
            QLabel, QLineEdit, QPushButton {
                color: lime;
                background-color: black;
            }
            QListView, QTreeView {
                background-color: black;
                color: lime;
            }
            QHeaderView::section {
                background-color: black;
                color: lime;
            }
            QScrollBar:vertical {
                background-color: black;
            }
            QScrollBar::handle:vertical {
                background-color: lime;
            }
        """)

        path = dialog.getExistingDirectory(self, "Select Music Folder")
        if path:
            try:
                songs = os.listdir(path)
                for song in songs:
                    if song.endswith(".mp3"):
                        self.playlist.addItem(os.path.join(path, song))
            except Exception as e:
                print(f"An error occurred: {e}")

    def set_position(self, position):
        self.is_slider_moving = True
        mixer.music.set_pos(position)
        self.is_slider_moving = False

    def play_music(self):
        global current_song_path
        current_item = self.playlist.currentItem()
        if current_item is not None:
            music_name = current_item.text()
            current_song_path = os.path.join(os.getcwd(), music_name)
            print(music_name[:-4])
            mixer.music.load(current_song_path)
            mixer.music.play()
            track_length = mixer.Sound(current_song_path).get_length()
            self.slider.setMaximum(int(track_length))
        else:
            print("No item selected")

    def set_volume(self, val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)

    def update_slider(self):
        if mixer.music.get_busy():
            current_position = mixer.music.get_pos() / 1000 
            self.slider.setValue(int(current_position))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec())
