from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QMessageBox
import sqlite3

class BookRegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Kayıt")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Barkod No:"))
        self.barcode_input = QLineEdit()
        layout.addWidget(self.barcode_input)

        layout.addWidget(QLabel("Kitap Adı:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Yazar:"))
        self.author_input = QLineEdit()
        layout.addWidget(self.author_input)

        layout.addWidget(QLabel("Yayın Evi:"))
        self.publisher_input = QLineEdit()
        layout.addWidget(self.publisher_input)

        layout.addWidget(QLabel("Basım Yılı:"))
        self.year_input = QLineEdit()
        layout.addWidget(self.year_input)

        layout.addWidget(QLabel("Kitap Adeti"))
        self.count_input = QLineEdit()
        layout.addWidget(self.count_input)

        self.save_button = QPushButton("Kaydet")
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_book)
        self.setLayout(layout)
        self.apply_styles()
    def save_book(self):
        # Giriş verilerini al
        barcode = self.barcode_input.text().strip()
        title = self.title_input.text().strip().title()
        author = self.author_input.text().strip().title()
        publisher = self.publisher_input.text().strip().title()
        year = self.year_input.text().strip()
        count = self.count_input.text().strip()

        # Boş alan kontrolü
        if not (barcode and title and author and publisher and year and count):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return

        try:
            # Sayısal alanları kontrol et
            year = int(year)
            count = int(count)
        except ValueError:
            QMessageBox.warning(self, "Geçersiz Veri", "Basım yılı ve kitap adeti sayı olmalıdır.")
            return

        # Veritabanı bağlantısı aç
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        # Aynı barkodlu kitap var mı kontrol et
        cursor.execute("SELECT barcode FROM books WHERE barcode = ?", (barcode,))
        existing = cursor.fetchone()
        if existing:
            QMessageBox.warning(self, "Zaten Kayıtlı", "Bu barkod numarasıyla bir kitap zaten kayıtlı.")
            conn.close()
            return

        # Veriyi ekle
        try:
            cursor.execute("INSERT INTO books (barcode, title, author, publisher, year, count) VALUES (?, ?, ?, ?, ?, ?)", 
                           (barcode, title, author, publisher, year, count))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Kitap başarıyla kaydedildi.")

            # Alanları temizle
            self.barcode_input.clear()
            self.title_input.clear()
            self.author_input.clear()
            self.publisher_input.clear()
            self.year_input.clear()
            self.count_input.clear()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
        finally:
            conn.close()
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
            QLabel {
                font-size: 15px;
                color: #2c3e50;
                font-weight: bold;
                padding: 4px;
                margin-bottom: 4px;
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