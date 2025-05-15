from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,QHeaderView
from PyQt5.QtGui import QColor
import sqlite3
from datetime import datetime
class CurrentStatusForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mevcut Durum")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        self.status_table = QTableWidget()
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(["Kitap", "Kimde", "Teslim Tarihi"])
        layout.addWidget(self.status_table)

        self.setLayout(layout)
        self.apply_styles()
        self.update_status()

    def update_status(self):
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        query = """
            SELECT books.title, users.adsoyad, loans.return_date
            FROM loans
            JOIN books ON loans.barcode = books.barcode
            JOIN users ON loans.tcno = users.tcno
        """
        cursor.execute(query)
        results = cursor.fetchall()
        print(len(results))
        self.status_table.setRowCount(len(results))
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(["Kitap", "Kimde", "Teslim Tarihi"])
        header = self.status_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # İçeriğe göre
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Kalan boşluğu alır
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        for i, (title, name, return_date) in enumerate(results):
            self.status_table.setItem(i, 0, QTableWidgetItem(title))
            self.status_table.setItem(i, 1, QTableWidgetItem(name))

            return_item = QTableWidgetItem(return_date)
            self.status_table.setItem(i, 2, return_item)  # Hücreyi önce tabloya ekle
            print(f"{i}: {return_date}")

            try:
                return_dt = datetime.strptime(return_date, "%Y-%m-%d")

                if return_dt.date() < datetime.today().date():
                    for col in range(self.status_table.columnCount()):
                        item = self.status_table.item(i, col)
                        if item:
                            item.setBackground(QColor("red"))
                            item.setForeground(QColor("white"))
            except Exception as e:
                print(f"{i}. satırda tarih formatı hatalı veya parse edilemedi:", e)

        conn.close()
    def apply_styles(self):
        style = """
            QWidget {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QLabel {
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
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
