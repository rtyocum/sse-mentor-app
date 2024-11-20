from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QWidget, QLabel


class TestCheckoutForm(QDialog):
    """A form to checkout a test. This form will be opened when a user scans their card."""

    user_id: str
    """The PK of the user that is checking out the test."""

    course_code: str
    """The course code of the test that is being checked out."""

    exam: str
    """Which exam is being checked out."""

    success: bool
    """Whether the form was successfully submitted."""

    def __init__(self, user: tuple, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Test Checkout")
        self.setFixedSize(400, 300)

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

        self.user_info_label = QLabel(f"{user[2]} {user[3]} ({user[1]})")
        self.form_layout.addRow("User:", self.user_info_label)

        self.course_code_input = QLineEdit()
        self.course_code_input.setPlaceholderText("Course Code")
        self.form_layout.addRow("Course Code:", self.course_code_input)

        self.exam_input = QLineEdit()
        self.exam_input.setPlaceholderText("Exam")
        self.form_layout.addRow("Exam:", self.exam_input)

        # Add submit button
        self.submit_button = QPushButton("Checkout")
        self.submit_button.clicked.connect(self.validate_submit_form)

        self.error_label = QLabel()
        self.error_label.hide()
        self.form_layout.addRow("", self.error_label)

        # Add layouts to main layout
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.submit_button)

        # Set dialog layout
        self.setLayout(self.main_layout)

    def validate_submit_form(self) -> None:
        """Validate the form and show a success message if successful."""
        # Check if all fields are filled out
        if self.course_code_input.text() and self.exam_input.text():
            self.course_code = self.course_code_input.text()
            self.exam = self.exam_input.text()

            self.course_code_input.clear()
            self.exam_input.clear()
            self.error_label.hide()
            self.success = True
            self.accept()
        else:
            self.error_label.setText("Please fill out all fields.")
            self.error_label.show()
