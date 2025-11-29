import sys
import os
import random
# pip install PyQt5 PyQtWebEngine folium geocoder
import folium
import geocoder
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

def get_location():
    """Vrati (lat, lon, metoda)"""
    try:
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            return g.latlng[0], g.latlng[1], "IP geolokacija"
    except:
        pass
    # ako nema interneta
    return random.uniform(-85, 85), random.uniform(-180, 180), "Slučajna lokacija (offline)"

class GPSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPS aplikacija (PyQt5)")
        self.resize(1000, 750)

        # Glavni vertikalni layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Gornji red: gumb + info
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.btn = QPushButton("📍 Lokacija")
        self.btn.setStyleSheet("""
            font-size: 14px;
            padding: 4px 10px;
        """)
        self.btn.clicked.connect(self.prikazi_lokaciju)

        self.label_coords = QLabel("Koordinate: —")
        self.label_coords.setStyleSheet("font-size: 11px; color: #333;")

        self.label_method = QLabel("Metoda: —")
        self.label_method.setStyleSheet("font-size: 11px; color: #555;")

        top_bar.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar.addWidget(self.label_coords)
        top_bar.addWidget(self.label_method)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # Web preglednik za kartu — zauzima ostatak prostora
        self.view = QWebEngineView()
        layout.addWidget(self.view, stretch=1)  # stretch=1 = širi se maksimalno

        # Početna prazna karta
        self.ucitaj_praznu_kartu()

    def ucitaj_praznu_kartu(self):
        mapa = folium.Map(location=[0, 0], zoom_start=2)
        mapa_file = "moja_lokacija.html"
        mapa.save(mapa_file)
        self.view.load(QUrl.fromLocalFile(os.path.abspath(mapa_file)))

    def prikazi_lokaciju(self):
        lat, lon, metoda = get_location()
        self.label_coords.setText(f"Koordinate: {lat:.6f}, {lon:.6f}")
        self.label_method.setText(f"Metoda: {metoda}")

        mapa = folium.Map(location=[lat, lon], zoom_start=14)
        folium.Marker(
            [lat, lon],
            popup=f"{metoda}\n({lat:.6f}, {lon:.6f})",
            tooltip="Tvoja lokacija"
        ).add_to(mapa)

        mapa_file = "moja_lokacija.html"
        mapa.save(mapa_file)
        self.view.load(QUrl.fromLocalFile(os.path.abspath(mapa_file)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPSApp()
    window.show()
    sys.exit(app.exec_())
