from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget

from typing import Tuple

# enum


class TestCheckinAction:
    RETURN = 1
    SWAP = 2


class TestCheckinDialog(QDialog):

    success: bool
    """Whether the form was successfully submitted."""

    action: int
    """The action to take."""

    test_checkout: Tuple[int, str, str]
    """The test that is being checked in."""

    def __init__(self, user: Tuple[int, str, str, str], test_checkout: Tuple[int, str, str], parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.test_checkout = test_checkout
        self.success = False
        self.action = 0

        self.setWindowTitle("Test Checkin")
        self.setFixedSize(600, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: #CCE1F6;
                color: #333333;  /* Dark gray text color */
            }
            QLabel {
                background-color: #CCE1F6;
                font-weight: bold;
                color: #333333;  /* Dark gray label color */
                font-size: 16px;
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

        self.user_info_label = QLabel(f"User: {user[2]} {user[3]} ({user[1]})")

        self.label = QLabel("Student has the test: " +
                            test_checkout[1] + " " + test_checkout[2] + ". What would you like to do?")
        self.label.setWordWrap(True)

        self.return_button = QPushButton("Return Test")
        self.return_button.clicked.connect(self.return_test)

        self.swap_button = QPushButton("Swap Test")
        self.swap_button.clicked.connect(self.swap_test)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        self.main_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.main_layout.addWidget(self.user_info_label)
        self.main_layout.addWidget(self.label)
        self.btn_layout.addWidget(self.return_button)
        self.btn_layout.addWidget(self.swap_button)
        self.btn_layout.addWidget(self.cancel_button)
        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout)

    def return_test(self) -> None:
        self.action = TestCheckinAction.RETURN
        self.success = True
        self.accept()

    def swap_test(self) -> None:
        self.action = TestCheckinAction.SWAP
        self.success = True
        self.accept()

    def cancel(self) -> None:
        self.accept()
