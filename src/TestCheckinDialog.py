from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

# enum
class TestCheckinAction:
    RETURN = 1
    SWAP = 2

class TestCheckinDialog(QDialog):

    success: bool
    """Whether the form was successfully submitted."""

    action: int
    """The action to take."""

    test_checkout: tuple

    def __init__(self, parent=None, test_checkout=None, user=None):
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

        self.label = QLabel("Student has the test: " + test_checkout[1] + " " + test_checkout[2] + ". What would you like to do?")
        self.label.setWordWrap(True)
        
        self.return_button = QPushButton("Return Test")
        self.return_button.clicked.connect(self.return_test)

        self.swap_button = QPushButton("Swap Test")
        self.swap_button.clicked.connect(self.swap_test)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)

        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        layout.addWidget(self.user_info_label)
        layout.addWidget(self.label)
        btn_layout.addWidget(self.return_button)
        btn_layout.addWidget(self.swap_button)
        btn_layout.addWidget(self.cancel_button)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def return_test(self):
        self.action = TestCheckinAction.RETURN
        self.success = True
        self.accept()
    
    def swap_test(self):
        self.action = TestCheckinAction.SWAP
        self.success = True
        self.accept()
    
    def cancel(self):
        self.accept()

