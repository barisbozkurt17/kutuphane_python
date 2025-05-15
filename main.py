import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from member_registration import MemberRegistrationForm
from book_registration import BookRegistrationForm
from book_lending import BookLendingForm
from book_return import BookReturnForm
from current_status import CurrentStatusForm
from createTable import create_database_and_tables

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kütüphane Yönetim Sistemi")
        self.setGeometry(100, 100, 400, 300)
        create_database_and_tables()
        layout = QVBoxLayout()
         # Logo ekleme
        self.logo_label = QLabel()
        logo_path = ".//dosyalar/logo.png"  # Dosya yolunu belirtiyoruz
        pixmap = QPixmap(logo_path)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedSize(200, 200)
        self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)  # Ortalamak için
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)    
        self.member_btn = QPushButton("Kişi Kayıt")
        self.member_btn.clicked.connect(self.open_member_form)
        layout.addWidget(self.member_btn)
        
        self.book_btn = QPushButton("Kitap Kayıt")
        self.book_btn.clicked.connect(self.open_book_form)
        layout.addWidget(self.book_btn)
        
        self.lending_btn = QPushButton("Kitap Verme")
        self.lending_btn.clicked.connect(self.open_lending_form)
        layout.addWidget(self.lending_btn)
        
        self.return_btn = QPushButton("Kitap Alma")
        self.return_btn.clicked.connect(self.open_return_form)
        layout.addWidget(self.return_btn)
        
        self.status_btn = QPushButton("Mevcut Durum")
        self.status_btn.clicked.connect(self.open_status_form)
        layout.addWidget(self.status_btn)
        
        self.setLayout(layout)
        self.apply_styles()
    def open_member_form(self):
        self.member_form = MemberRegistrationForm()
        self.member_form.show()
    
    def open_book_form(self):
        self.book_form = BookRegistrationForm()
        self.book_form.show()
    
    def open_lending_form(self):
        self.lending_form = BookLendingForm()
        self.lending_form.show()
    
    def open_return_form(self):
        self.return_form = BookReturnForm()
        self.return_form.show()
    
    def open_status_form(self):
        self.status_form = CurrentStatusForm()
        self.status_form.show()
    def apply_styles(self):
        style = """
            QWidget {
                background-color: #f5f5f5;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 3px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db; /* Mavi kenarlık */
                background-color: #eaf6ff; /* Hafif mavi arka plan */
                color: #000000; /* Yazı rengi siyah olabilir */
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: white;
            }
            QTabBar::tab {
                background: #ddd;
                padding: 5px;
                border: 1px solid #bbb;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #fff;
                border-bottom-color: white;
            }
        """
        self.setStyleSheet(style)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
