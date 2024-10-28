import sys
import os

import colorsys
import datetime
import webbrowser
import re
import random

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QDialog, QPushButton
from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtGui import QKeyEvent, QCloseEvent
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

TITLE_FONT_SIZE = 80
"""The font size of the title text in pixels."""

TIME_FONT_SIZE = 40
"""The font size of the time text in pixels."""

SONGS_FOLDER = "/data/Songs/"
"""The folder where the songs are stored."""

SONGS_FOLDER_FRIDAY = "/data/Songs/Friday/"
"""The folder where the friday songs are stored."""

LAB_HEADCOUNT_TIME = 30
"""The time in minutes when the lab headcount is triggered. (Usually 30 minutes)"""

MENTEE_HEADCOUNT_TIME = 55
"""The time in minutes when the mentee headcount is triggered. (Usually 55 minutes)"""


# TODO: Create a form to checkout a test
class TestCheckoutForm(QDialog):
    """A form to checkout a test. This form will be opened when a user scans their card."""

    uid: str
    """The UID of the user that is checking out the test."""

    def __init__(self, parent: QWidget | None = None, uid: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle("QDialog")
        self.uid = uid

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
        self.media_player.mediaStatusChanged.connect(lambda status: self.close() if status == QMediaPlayer.MediaStatus.EndOfMedia else None)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # layout
        self.main_layout = QVBoxLayout(self)

        self.setStyleSheet("background-color: black;")

        # add a label
        self.label = QLabel("Headcount Time!")
        
        # no background color/transparent
        self.label.setStyleSheet("font-size: 40px; color: white;")
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
        self.media_player.setSource(QUrl.fromLocalFile(os.path.join(directory, random_file)))
        self.media_player.play()

    
    def closeEvent(self, event: QCloseEvent | None) -> None:
        """Override the close event to stop the media player when the dialog is closed."""
        self.media_player.stop()
        
        if event is not None:
            event.accept()


class MentorWindow(QMainWindow):

    current_minute: int
    """The current minute of the system time. Used to open the browser at the right time."""

    current_hue: float
    """The current hue of the background color. Used do the scrolling color."""

    time_key_has_text: int
    """The time the key has text. Used to clear the key_string after a while. This allows only the card reader to input text, and not the keyboard."""

    key_string: str
    """The string that is being input by the card reader."""

    def __init__(self) -> None:
        super().__init__()

        # Creaton
        self.setWindowTitle("Mentor App")

        # Will eventually be full screen, but for now, it is a window.
        self.showFullScreen()

        # Set the window size to match the screen size and fix it
        self.setFixedSize(1920, 1080)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # initialize variables
        self.current_minute = 0
        self.current_hue = 0
        self.time_key_has_text = 0
        self.key_string = ""

        # start the color change timer and set event (update is called every 30ms)
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self.update_window)
        self.color_timer.start(30)

        # layout
        self.main_layout = QVBoxLayout(centralWidget)
        self.main_layout.addStretch()

        # title (the big text in the middle)
        self.titleLabel = QLabel("Hello, Mentor!")
        self.titleLabel.setStyleSheet(f"font-size: {TITLE_FONT_SIZE}px; color: black;")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)


        self.main_layout.addStretch()

        # time label (the small text at the bottom)
        self.timeLabel = QLabel("00:00:00")
        self.timeLabel.setStyleSheet(f"font-size: {TIME_FONT_SIZE}px; color: black;")
        self.timeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.timeLabel, alignment=Qt.AlignmentFlag.AlignBottom)


    def update_window(self) -> None:
        """Update the window. This is initialized in __init__ and is called every 30ms."""

        self.change_background_color()

        # get current time
        current_time = datetime.datetime.now()
        minutes = current_time.minute
        is_friday = current_time.weekday() == 4

        # clear the key string after a while. Clears it in case someone accidentally types on the keyboard.
        if (self.key_string != ""):
            self.time_key_has_text += 1

        if (self.time_key_has_text > 100):
            self.key_string = ""
            self.time_key_has_text = 0


        # open the browser at the right time. current_minute is used to prevent the browser from opening multiple times in the same minute.
        if (minutes == 23 and minutes != self.current_minute):
            # open the browser
            self.current_minute = minutes
            webbrowser.open("https://forms.gle/Zem6tQbCTEsBpoza6")
            headcount_dialog = HeadcountDialog(is_friday, self)
            headcount_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            headcount_dialog.show()
        elif (minutes == 55 and minutes != self.current_minute):
            # open the browser
            self.current_minute = minutes
            webbrowser.open("https://forms.gle/Zem6tQbCTEsBpoza6")
            headcount_dialog = HeadcountDialog(is_friday, self)
            headcount_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            headcount_dialog.show()

        # get the current time as a string
        string_time = current_time.strftime("%H:%M:%S")

        # update the time label
        self.timeLabel.setText(string_time)

    def change_background_color(self) -> None:
        """Change the background color of the window."""

        # Increment the hue by 0.5, if it is 360, set it to 0.
        self.current_hue = (self.current_hue + 0.5) % 360

        # Convert the hue to an RGB color
        new_color = colorsys.hls_to_rgb(self.current_hue / 360, 0.5, 0.2)

        # Set the background color of the window
        color =  f'rgb({new_color[0] * 255}, {new_color[1] * 255}, {new_color[2] * 255})'
        self.setStyleSheet(f'background-color: {color}')

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        """Override to listen for key press events. This is used to listen for card reader input."""

        if event is None:
            return

        if event.key() == Qt.Key.Key_Return:
            self.check_uid(self.key_string)
            self.key_string = ""
        else:
            self.key_string += event.text()

    def check_uid(self, card_data: str) -> None:
        """Currently work in progress. This function is called when the whole UID is input by the card reader."""
        # Check if the UID is valid. See README.md for more information on the card format.
        match = re.match(r"^;([0-9]{9})=[0-9]{4}\?$", card_data)
        uid = match.group(1) if match else None

        if uid:
            # do something with the UID
            TestCheckoutForm(self, uid).show()
        



def main() -> None:
    """Mentor App's main function."""
    mentorApp = QApplication([])
    mentorWindow = MentorWindow()
    mentorWindow.show()
    sys.exit(mentorApp.exec())


if __name__ == "__main__":
    main()
