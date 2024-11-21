from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QCloseEvent
import os
import random

SONGS_FOLDER = "C:\\Users\\sse-mentor\\headcounttest\\Songs"
"""The folder where the songs are stored."""

SONGS_FOLDER_FRIDAY = "C:\\Users\\sse-mentor\\headcounttest\Songs\\Friday"
"""The folder where the friday songs are stored."""


class HeadcountDialog(QDialog):
    """A dialog that opens when the headcount gets triggered. Handle playing the song"""

    media_player: QMediaPlayer
    """The media player that plays the sound."""

    audio_output: QAudioOutput
    """The audio output that plays the sound."""

    is_friday: bool
    """Whether it is Friday or not."""

    def __init__(self, is_friday: bool, parent: QWidget | None = None) -> None:

        super().__init__(parent)

        self.is_friday = is_friday

        self.setWindowTitle("Headcount Time!")

        # initialize the media player
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # close the dialog when the song ends
        self.media_player.mediaStatusChanged.connect(lambda status: self.close(
        ) if status == QMediaPlayer.MediaStatus.EndOfMedia else None)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # layout
        self.main_layout = QVBoxLayout(self)

        self.setStyleSheet("""
            QDialog {
                background-color: #CCE1F6;
                color: #333333;  /* Dark gray text color */
            }
            QLabel {
                background-color: #CCE1F6;
                font-weight: bold;
                color: #333333;  /* Dark gray label color */
                font-size: 64px;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                padding: 5px;
                color: #333333;
                font-size: 16px;
            }
            QPushButton {
                background-color: #0669D3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0447B1;
            }
        """)

        # add a label
        self.label = QLabel("Headcount Time!")

        # no background color/transparent
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.close)
        self.main_layout.addWidget(self.ok_button)

        self.play_random_sound()

    def play_random_sound(self) -> None:
        """Play a random sound. This is used to play a sound at 30m and 55m."""

        directory = SONGS_FOLDER_FRIDAY if self.is_friday else SONGS_FOLDER

        # pick a random sound
        files = os.listdir(directory)

        files = [f for f in files if f.endswith(".mp3")]

        if len(files) == 0:
            return

        random_file = random.choice(files)

        # play the sound
        self.media_player.setSource(QUrl.fromLocalFile(
            os.path.join(directory, random_file)))
        self.media_player.play()

    def closeEvent(self, event: QCloseEvent | None) -> None:
        """Override the close event to stop the media player when the dialog is closed."""
        self.media_player.stop()

        if event is not None:
            event.accept()
