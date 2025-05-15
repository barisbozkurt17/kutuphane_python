from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QMessageBox
import sqlite3
class MemberRegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kişi Kayıt")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("TC No:"))
        self.tc_no_input = QLineEdit()
        layout.addWidget(self.tc_no_input)

        layout.addWidget(QLabel("Ad Soyad:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Telefon Numarası:"))
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_input)

        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_members)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.apply_styles()

    def save_members(self):
        # Giriş verilerini al
        tc_no = self.tc_no_input.text().strip()
        adsoyad = self.name_input.text().strip().title()
        phone = self.phone_input.text().strip()

        # Boş alan kontrolü
        if not (tc_no and adsoyad and phone):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return


        if not (tc_no.isdigit() and len(tc_no) == 11 and tc_no[0] != '0'):
            QMessageBox.warning(self, "Geçersiz TC No", "Lütfen geçerli bir 11 haneli T.C. Kimlik Numarası girin.")
            return

        # Veritabanı bağlantısı aç
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        # Aynı barkodlu kitap var mı kontrol et
        cursor.execute("SELECT adsoyad FROM users WHERE tcno = ?", (tc_no,))
        existing = cursor.fetchone()
        if existing:
            adsoyad = existing[0]
            QMessageBox.warning(self, "Zaten Kayıtlı", f"Bu T.C. no ile {adsoyad} adlı kişi zaten kayıtlı.")
            conn.close()
            return
        # Veriyi ekle
        try:
            cursor.execute("INSERT INTO users (tcno, adsoyad, telefon) VALUES (?, ?, ?)", 
                           (tc_no, adsoyad, phone))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Kitap başarıyla kaydedildi.")

            # Alanları temizle
            self.tc_no_input.clear()
            self.name_input.clear()
            self.phone_input.clear()


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