from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Password")
        self.setFixedSize(300, 150)
        
        self.label = QLabel("Enter Mentor Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_password)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)
        
        self.password_correct = False  # Flag to indicate password success
    
    def check_password(self):
        # Set your actual password here (in a real application, this should be securely handled)
        actual_password = "M3nt0r5Rock!"
        if self.password_input.text() == actual_password:
            self.password_correct = True
            self.accept()
        else:
            self.label.setText("Incorrect password. Try again.")
            self.password_input.clear()

