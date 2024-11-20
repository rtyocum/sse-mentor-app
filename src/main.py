import sys
import sqlite3

from PyQt6.QtWidgets import QApplication

from MentorWindow import MentorWindow


LAB_HEADCOUNT_TIME = 30
"""The time in minutes when the lab headcount is triggered. (Usually 30 minutes)"""

MENTEE_HEADCOUNT_TIME = 55
"""The time in minutes when the mentee headcount is triggered. (Usually 55 minutes)"""


def main() -> None:
    """Mentor App's main function."""

    db_conn = sqlite3.connect("./mentor.db")

    mentorApp = QApplication([])
    mentorWindow = MentorWindow(db_conn)
    mentorWindow.show()
    sys.exit(mentorApp.exec())


if __name__ == "__main__":
    main()
