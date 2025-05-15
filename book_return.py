from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog, QTableWidget, QTableWidgetItem,QFormLayout
import sqlite3

class BookReturnForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap İade")
        self.setGeometry(200, 200, 400, 200)

        # Form düzeni (etiket ve alanları yatay hizalar)
        form_layout = QFormLayout()

        self.barcode_input = QLineEdit()
        form_layout.addRow("Kitap Barkod No:", self.barcode_input)

        # Ana dikey düzen
        layout = QVBoxLayout()
        layout.addLayout(form_layout)

        # Buton alt satırda ortalı şekilde
        self.return_button = QPushButton("İade Al")
        layout.addWidget(self.return_button)

        self.return_button.clicked.connect(self.iadeAl)

        self.setLayout(layout)
        self.apply_styles()

    def iadeAl(self):
        barcode = self.barcode_input.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Uyarı", "Barkod giriniz!")
            return

        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, tcno FROM loans WHERE barcode = ?", (barcode,))
        records = cursor.fetchall()

        if not records:
            QMessageBox.information(self, "Bilgi", "Bu barkodla ödünç alınmış bir kitap bulunamadı.")
            conn.close()
            return

        if len(records) == 1:
            self.return_book(records[0][0], barcode, conn)
        else:
            self.choose_borrower(records, barcode, conn)

    def return_book(self, loan_id, barcode, conn):
        cursor = conn.cursor()
        # loans tablosundan kaydı sil
        cursor.execute("DELETE FROM loans WHERE id = ?", (loan_id,))
        # books tablosundaki count değerini 1 artır
        cursor.execute("UPDATE books SET count = count + 1 WHERE barcode = ?", (barcode,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Başarılı", "Kitap iade alındı ve stok güncellendi.")

    def choose_borrower(self, records, barcode, conn):
        dialog = QDialog(self)
        dialog.setWindowTitle("Kullanıcı Seçimi")
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(len(records))
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Sira No","Ad Soyad", "TC No"])
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for i, (loan_id, tcno) in enumerate(records):
            table.setItem(i, 0, QTableWidgetItem(str(loan_id)))
            records  = conn.cursor().execute("SELECT adsoyad FROM users WHERE tcno = ?", (tcno,)).fetchall()
            table.setItem(i, 1, QTableWidgetItem(records[0][0]))
            table.setItem(i, 2, QTableWidgetItem(str(tcno)))

        table.cellDoubleClicked.connect(lambda row, col: self.select_loan(row, table, barcode, dialog, conn))
        layout.addWidget(QLabel("Bu kitabı birden fazla kişi almış. Kimin teslim ettiğini seçin:"))
        layout.addWidget(table)
        dialog.setLayout(layout)
        self.apply_styles()
        dialog.exec_()

    def select_loan(self, row, table, barcode, dialog, conn):
        loan_id_item = table.item(row, 0)
        if loan_id_item:
            loan_id = int(loan_id_item.text())
            self.return_book(loan_id, barcode, conn)
            dialog.accept()
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
        self.setStyleSheet(style)
