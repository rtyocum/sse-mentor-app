from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QWidget, QLabel


class UserRegistration(QDialog):
    """A form to checkout a test. This form will be opened when a user scans their card."""

    uid: str
    """The UID of the user that is checking out the test."""

    first_name: str
    """The first name of the user that is checking out the test."""

    last_name: str
    """The last name of the user that is checking out the test."""

    email: str
    """The email of the user that is checking out the test."""

    success: bool
    """Whether the form was successfully submitted."""

    def __init__(self, parent: QWidget | None = None, uid: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle("User Registration")
        self.setFixedSize(600, 300)
        self.success = False

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

        # Set up layout
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Add form fields

        # UID Field with "Show" Button
        self.uid_input = QLineEdit()
        self.uid_input.setPlaceholderText("Enter your UID")
        self.uid_input.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.uid_input.setText(uid)
        self.form_layout.addRow("UID:", self.uid_input)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.form_layout.addRow("First Name:", self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.form_layout.addRow("Last Name:", self.last_name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter user's email")
        self.form_layout.addRow("Email:", self.email_input)

        # Add submit button
        self.submit_button = QPushButton("Register")
        self.submit_button.clicked.connect(self.validate_submit_form)

        self.error_label = QLabel()
        self.error_label.hide()
        self.form_layout.addRow("", self.error_label)

        # Add layouts to main layout
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.submit_button)

        # Set dialog layout
        self.setLayout(self.main_layout)

        # set focus to the first name field
        self.first_name_input.setFocus()

    def validate_submit_form(self) -> None:
        """Validate the form and show a success message if successful."""
        # Check if all fields are filled out
        if self.uid_input.text() and self.first_name_input.text() and self.last_name_input.text() and self.email_input.text():
            self.uid = self.uid_input.text()
            self.first_name = self.first_name_input.text()
            self.last_name = self.last_name_input.text()
            self.email = self.email_input.text()

            self.uid_input.clear()
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.email_input.clear()
            self.error_label.hide()
            self.success = True
            self.accept()
        else:
            self.error_label.setText("Please fill out all fields.")
            self.error_label.show()
