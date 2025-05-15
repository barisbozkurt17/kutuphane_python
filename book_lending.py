import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QMessageBox,QHeaderView

class BookLendingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Verme")
        self.setGeometry(200, 200, 500, 350)

        layout = QVBoxLayout()

        # Kitap Barkod Alanı
        layout.addWidget(QLabel("Kitap Barkod No:"))
        self.barcode_input = QLineEdit()
        layout.addWidget(self.barcode_input)

        # Kitap Arama Butonu
        self.book_search_button = QPushButton("Kitap Ara")
        self.book_search_button.clicked.connect(lambda: self.open_search_window("books"))
        layout.addWidget(self.book_search_button)

        # Öğrenci TC No Alanı
        layout.addWidget(QLabel("Okuyucu TC No:"))
        self.tc_input = QLineEdit()
        layout.addWidget(self.tc_input)

        # Öğrenci Arama Butonu
        self.user_search_button = QPushButton("Okuyucu Ara")
        self.user_search_button.clicked.connect(lambda: self.open_search_window("members"))
        layout.addWidget(self.user_search_button)

        # Ödünç Verme Butonu
        self.lend_button = QPushButton("Ödünç Ver")
        layout.addWidget(self.lend_button)
        self.lend_button.clicked.connect(self.lend_book)

        self.setLayout(layout)
        self.apply_styles()

    def open_search_window(self, search_type):
        """Kitap veya Okuyucu arama penceresini açar."""
        search_window = SearchWindow(search_type, self)
        search_window.exec_()

    def lend_book(self):
        tcno = self.tc_input.text().strip()
        barcode = self.barcode_input.text().strip()

        if not tcno or not barcode:
            QMessageBox.warning(self, "Eksik Bilgi", "T.C. no ve barkod no boş bırakılamaz.")
            return

        try:
            conn = sqlite3.connect("db.db", timeout=10)
            conn.row_factory = sqlite3.Row  # Satırları sözlük gibi kullanabilmek için
            cursor = conn.cursor()

            # Kullanıcı var mı?
            cursor.execute("SELECT * FROM users WHERE tcno = ?", (tcno,))
            user = cursor.fetchone()
            if not user:
                QMessageBox.warning(self, "Kullanıcı Yok", "Bu T.C. numarası ile kayıtlı kullanıcı bulunamadı.")
                return
            if user["mevcut"] > 2:
                QMessageBox.warning(self, "Fazla Kitap", "Maksimum kitap hakkı 3'tür.")
                return

            # Kitap var mı?
            cursor.execute("SELECT * FROM books WHERE barcode = ?", (barcode,))
            book = cursor.fetchone()
            if not book:
                QMessageBox.warning(self, "Kitap Yok", "Bu barkod numarası ile kayıtlı kitap bulunamadı.")
                return

            # Aynı kitap zaten bu kullanıcıda mı?
            cursor.execute("SELECT * FROM loans WHERE tcno = ? AND barcode = ?", (tcno, barcode))
            loan = cursor.fetchone()
            if loan:
                QMessageBox.warning(self, "Zaten Ödünç Verilmiş", "Bu kitap zaten bu kullanıcıda.")
                return

            # Kitap stokta var mı?
            if book["count"] <= 0:
                QMessageBox.warning(self, "Kitap Mevcut Değil", "Bu kitap şu anda mevcut değil.")
                return

            # Tarihleri belirle
            borrow_date = datetime.today().strftime("%Y-%m-%d")
            return_date = (datetime.today() + timedelta(days=15)).strftime("%Y-%m-%d")

            # loans tablosuna ekle
            cursor.execute(
                "INSERT INTO loans (tcno, barcode, borrow_date, return_date) VALUES (?, ?, ?, ?)",
                (tcno, barcode, borrow_date, return_date)
            )

            # books tablosunu güncelle
            cursor.execute(
                "UPDATE books SET count = count - 1, read_count = read_count + 1 WHERE barcode = ?",
                (barcode,)
            )

            # users tablosunu güncelle
            cursor.execute(
                "UPDATE users SET mevcut = mevcut + 1, okunan = okunan + 1 WHERE tcno = ?",
                (tcno,)
            )

            conn.commit()
            QMessageBox.information(self, "Başarılı", "Kitap ödünç verildi.")

            self.tc_input.clear()
            self.barcode_input.clear()
            self.tc_input.setFocus()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu:\n{e}")
        
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
class SearchWindow(QDialog):
    def __init__(self, search_type, parent):
        super().__init__()
        self.setWindowTitle("Arama")
        self.setGeometry(250, 250, 450, 300)
        self.parent = parent
        self.search_type = search_type  # "books" veya "members"

        layout = QVBoxLayout()
        
        # Arama Kutusu
        self.search_label = QLabel(f"{'Kitap' if search_type == 'books' else 'Okuyucu'} Adı:")
        layout.addWidget(self.search_label)

        # Arama button u iptal. Text ile arama. 
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ara")
        self.search_input.textChanged.connect(self.search_database)
        layout.addWidget(self.search_input)


        # Sonuç Tablosu
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)

        if search_type == "books":
            self.result_table.setHorizontalHeaderLabels(["Barkod", "Kitap Adı"])
            
        else:
            self.result_table.setHorizontalHeaderLabels(["TC No", "Ad Soyad"])
        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # İçeriğe göre
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Kalan boşluğu alır
        self.search_database()
        self.result_table.cellDoubleClicked.connect(self.select_item)
        layout.addWidget(self.result_table)

        self.setLayout(layout)
        self.apply_styles()

    def search_database(self):
        """Veritabanında kitap veya öğrenci araması yapar."""
        search_text = self.search_input.text()
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        #Kitap databasede arama yapıyor.
        if self.search_type == "books":
            query = "SELECT barcode, title FROM books WHERE LOWER(title) LIKE LOWER(?) OR barcode LIKE ?"
        else:
            query = "SELECT tcno, adsoyad FROM users WHERE LOWER(adsoyad) LIKE LOWER(?) OR tcno LIKE ?"
            
        param = f"%{search_text.lower()}%"
        cursor.execute(query, (param, param))
        results = cursor.fetchall()
        conn.close()
        
        # Sonuçları tabloya ekle
        self.result_table.setRowCount(len(results))
        for row_index, row_data in enumerate(results):
            for col_index, col_value in enumerate(row_data):
                self.result_table.setItem(row_index, col_index, QTableWidgetItem(str(col_value)))
        self.result_table.resizeColumnsToContents() 
    def select_item(self, row, column):
        """Çift tıklanınca ilgili bilgiyi ana pencereye aktarır."""
        selected_value = self.result_table.item(row, 0).text()  # Barkod veya TC No
        
        if self.search_type == "books":
            self.parent.barcode_input.setText(selected_value)
        else:
            self.parent.tc_input.setText(selected_value)

        self.close()
    def apply_styles(self):
        style = """
            QWidget {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QLabel {
                font-size: 15px;
                color: #2c3e50;
                font-weight: bold;
                padding: 4px;
                margin-bottom: 4px;
            }
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 6px;
                background-color: #ffffff;
            }

            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: #eaf6ff;
            }

            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                gridline-color: #dcdcdc;
            }

            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 4px;
            }

            QTableWidget::item:selected {
                background-color: #d0ebff;
                color: #2c3e50;
            }

            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #27ae60;
            }

            QPushButton:pressed {
                background-color: #1e8449;
            }
        """
        self.setStyleSheet(style)

