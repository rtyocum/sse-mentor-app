from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QDialog
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QKeyEvent
import webbrowser
import datetime
import colorsys
import re
import hashlib
import json
import jwt
import requests
from sqlite3 import Connection
from TestCheckinDialog import TestCheckinDialog, TestCheckinAction
from TestCheckoutForm import TestCheckoutForm
from UserRegistration import UserRegistration
from HeadcountDialog import HeadcountDialog
from typing import Tuple

TITLE_FONT_SIZE = 80
"""The font size of the title text in pixels."""

TIME_FONT_SIZE = 40
"""The font size of the time text in pixels."""


class MentorWindow(QMainWindow):

    current_minute: int
    """The current minute of the system time. Used to open the browser at the right time."""

    current_hue: float
    """The current hue of the background color. Used do the scrolling color."""

    time_key_has_text: int
    """The time the key has text. Used to clear the key_string after a while. This allows only the card reader to input text, and not the keyboard."""

    key_string: str
    """The string that is being input by the card reader."""

    db_conn: Connection
    """The database connection."""

    def __init__(self, db_conn: Connection) -> None:
        super().__init__()

        self.db_conn = db_conn

        # Creaton
        self.setWindowTitle("Mentor App")

        # Will eventually be full screen, but for now, it is a window.
        # self.showFullScreen()

        # Set the window size to match the screen size and fix it
        self.setGeometry(0, 0, 1920, 1080)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # initialize variables

        # -1, not 0, otherwise browser won't open if ever triggered at 0 minutes
        self.current_minute = -1
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
        self.titleLabel = QLabel("Hello, Mentor! Swipe a card")
        self.titleLabel.setStyleSheet(
            f"font-size: {TITLE_FONT_SIZE}px; color: black;")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch()

        # time label (the small text at the bottom)
        self.timeLabel = QLabel("00:00:00")
        self.timeLabel.setStyleSheet(
            f"font-size: {TIME_FONT_SIZE}px; color: black;")
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
        if (minutes == 30 and minutes != self.current_minute):
            # open the browser
            self.current_minute = minutes
            webbrowser.open("https://forms.gle/Zem6tQbCTEsBpoza6", new=1)
            headcount_dialog = HeadcountDialog(is_friday, self)
            headcount_dialog.setWindowModality(
                Qt.WindowModality.ApplicationModal)
            headcount_dialog.show()
        elif (minutes == 55 and minutes != self.current_minute):
            # open the browser
            self.current_minute = minutes
            webbrowser.open("https://forms.gle/Zem6tQbCTEsBpoza6", new=1)
            headcount_dialog = HeadcountDialog(is_friday, self)
            headcount_dialog.setWindowModality(
                Qt.WindowModality.ApplicationModal)
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
        color = f'rgb({new_color[0] * 255}, {new_color[1]
                                             * 255}, {new_color[2] * 255})'
        self.setStyleSheet(f'background-color: {color}')

    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        """Override to listen for key press events. This is used to listen for card reader input."""

        if event is None:
            return

        # If the key is the return key, check the UID.

        if event.key() == Qt.Key.Key_Return:
            self.check_uid(self.key_string)
            self.key_string = ""
        else:
            self.key_string += event.text()

    def check_uid(self, card_data: str) -> None:
        """This function is called when the whole UID is input by the card reader. It checks if the UID is valid and then checks in or checks out the user."""

        # Check if the UID is valid. See README.md for more information on the card format.
        match = re.match(r"^;([0-9]{9})=[0-9]{4}\?$", card_data)
        uid = match.group(1) if match else None

        if uid:
            user = self.get_user_by_uid(uid)

            if user:
                test_checkout = self.get_current_test(user[0])

                if test_checkout:
                    print("Test found!")
                    self.checkin_test(user, test_checkout)
                else:
                    self.checkout_test(user)

            else:
                user = self.register_user(uid)
                if user == None:
                    return
                self.checkout_test(user)

    def checkin_test(self, user: Tuple[int, str, str, str], test_checkout: Tuple[int, str, str]) -> None:
        """Check in a test for the given user."""
        test_checkin = TestCheckinDialog(user, test_checkout, self)
        if test_checkin.exec() == QDialog.DialogCode.Accepted and test_checkin.success:
            if test_checkin.action == TestCheckinAction.RETURN:
                cursor = self.db_conn.execute(
                    "UPDATE testcheckout SET checkin_date = ? WHERE ID = ?", (datetime.datetime.now(), test_checkout[0]))
                self.db_conn.commit()
                cursor.close()
                self.publish_record(test_checkout[0])
            elif test_checkin.action == TestCheckinAction.SWAP:
                success = self.checkout_test(user)
                if success:
                    cursor = self.db_conn.execute(
                        "UPDATE testcheckout SET checkin_date = ? WHERE ID = ?", (datetime.datetime.now(), test_checkout[0]))
                    self.db_conn.commit()
                    cursor.close()
                    self.publish_record(test_checkout[0])

    def checkout_test(self, user: tuple) -> bool:
        """Checkout a test for the given user."""
        test_checkout = TestCheckoutForm(user, self)
        if test_checkout.exec() == QDialog.DialogCode.Accepted and test_checkout.success:
            cursor = self.db_conn.execute("INSERT INTO testcheckout (user_id, course_code, test_name, checkout_date) VALUES (?, ?, ?, ?)", (
                user[0], test_checkout.course_code, test_checkout.exam, datetime.datetime.now()))
            self.db_conn.commit()

            row_id = cursor.lastrowid
            cursor.close()

            if row_id:
                self.publish_record(row_id)
                return True

        return False

    def get_current_test(self, user_id: int) -> Tuple[int, str, str]:
        """Get the current test that the user has checked out."""
        cursor = self.db_conn.execute(
            "SELECT ID, COURSE_CODE, TEST_NAME FROM testcheckout WHERE user_id = ? AND checkin_date IS NULL", (user_id,))
        test: Tuple[int, str, str] = cursor.fetchone()
        cursor.close()
        return test

    def get_user_by_uid(self, uid: str) -> Tuple[int, str, str, str]:
        """Get a user by the given UID."""
        hashed_uid = hashlib.sha512(uid.encode()).hexdigest()
        cursor = self.db_conn.execute(
            "SELECT ID, EMAIL, FIRSTNAME, LASTNAME FROM users WHERE uid = ?", (hashed_uid,))
        user: Tuple[int, str, str, str] = cursor.fetchone()
        cursor.close()
        return user

    def register_user(self, uid: str) -> Tuple[int, str, str, str] | None:
        """Register a user with the given UID."""
        user_registration = UserRegistration(self, uid)

        if user_registration.exec() == QDialog.DialogCode.Accepted and user_registration.success:
            hashed_uid = hashlib.sha512(
                user_registration.uid.encode()).hexdigest()
            cursor = self.db_conn.execute("INSERT INTO users (uid, firstname, lastname, email) VALUES (?, ?, ?, ?)", (
                hashed_uid, user_registration.first_name, user_registration.last_name, user_registration.email))
            self.db_conn.commit()

            row_id = cursor.lastrowid
            cursor.close()

            # grab the user id
            cursor = self.db_conn.execute(
                "SELECT ID, EMAIL, FIRSTNAME, LASTNAME FROM users WHERE ID = ?", (row_id,))
            user: Tuple[int, str, str, str] = cursor.fetchone()
            cursor.close()

            return user
        return None

    def publish_record(self, test_checkout_id: int) -> None:
        """Publish the record of the user checking in a test."""

        sql = "SELECT tc.SHEETS_RANGE, tc.COURSE_CODE, tc.TEST_NAME, tc.CHECKOUT_DATE, tc.CHECKIN_DATE, u.FIRSTNAME, u.LASTNAME, u.EMAIL FROM testcheckout tc JOIN users u ON tc.USER_ID = u.ID WHERE tc.ID = ?"
        cursor = self.db_conn.execute(sql, (test_checkout_id,))
        record = cursor.fetchone()
        cursor.close()

        config = None
        with open("D:\\config.json") as f:
            config = json.load(f)

        payload = {
            "iss": config["client_email"],
            "scope": "https://www.googleapis.com/auth/spreadsheets",
            "aud": "https://oauth2.googleapis.com/token",
            "exp": int((datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp()),
            "iat": int(datetime.datetime.now().timestamp())
        }

        token = jwt.encode(payload, config["private_key"], algorithm="RS256")

        res = requests.post("https://oauth2.googleapis.com/token", json={
                            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": token})
        res.raise_for_status()

        access_token = res.json()["access_token"]

        sheetId = '19JxzCcRoHgtTkXTjHmZ5yKhftTqy2ku9438W6v4NDv8'
        range = 'A1'

        if record[0] is None:

            res = requests.post(f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/{range}:append?valueInputOption=USER_ENTERED", json={
                "values": [
                    [record[1], record[2], record[3], record[4],
                        record[5], record[6], record[7]]
                ]
            }, headers={"Authorization": f"Bearer {access_token}"})

            print(res.json())

            res.raise_for_status()

            cursor = self.db_conn.execute("UPDATE testcheckout SET SHEETS_RANGE = ? WHERE ID = ?", (res.json()[
                                          'updates']['updatedRange'], test_checkout_id))

            self.db_conn.commit()
            cursor.close()
        else:
            res = requests.put(f"https://sheets.googleapis.com/v4/spreadsheets/{sheetId}/values/{record[0]}?valueInputOption=USER_ENTERED", json={
                "values": [
                    [record[1], record[2], record[3], record[4],
                        record[5], record[6], record[7]]
                ]
            }, headers={"Authorization": f"Bearer {access_token}"})

            res.raise_for_status()
