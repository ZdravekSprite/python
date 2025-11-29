import sys
import os
import random
import requests
import folium
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt


def get_location():
    """Vrati (lat, lon, opis, metoda) — koristi ipinfo + OSM."""
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        if r.ok:
            data = r.json()
            if "loc" in data:
                lat, lon = map(float, data["loc"].split(","))
                opis = get_address_from_osm(lat, lon) or data.get("city", "Nepoznato")
                return lat, lon, opis, "IP + OpenStreetMap"
    except Exception as e:
        print("Greška kod dohvaćanja IP lokacije:", e)

    # Offline fallback
    lat, lon = random.uniform(-85, 85), random.uniform(-180, 180)
    return lat, lon, "Slučajna lokacija (offline)", "Offline način"


def get_address_from_osm(lat, lon):
    """Vrati adresu pomoću OpenStreetMap Nominatim API-ja."""
    try:
        url = (
            f"https://nominatim.openstreetmap.org/reverse"
            f"?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1"
        )
        r = requests.get(url, headers={"User-Agent": "PyQtGPSApp/1.0"}, timeout=5)
        if r.ok:
            data = r.json()
            return data.get("display_name")
    except Exception as e:
        print("Greška kod OSM reverse geocodinga:", e)
    return None


def get_temperature(lat, lon):
    """Vrati temperaturu na zadanim koordinatama (Open-Meteo API)."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        r = requests.get(url, timeout=5)
        if r.ok:
            data = r.json()
            if "current_weather" in data:
                return data["current_weather"]["temperature"]
    except Exception as e:
        print("Greška kod dohvaćanja temperature:", e)
    return None


class GPSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPS aplikacija + Temperatura (OSM + Open-Meteo)")
        self.resize(1000, 750)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # Gornji red
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.btn = QPushButton("📍 Lokacija + 🌡️ Temperatura")
        self.btn.setStyleSheet("font-size: 14px; padding: 4px 10px;")
        self.btn.clicked.connect(self.prikazi_lokaciju)

        self.label_coords = QLabel("Koordinate: —")
        self.label_coords.setStyleSheet("font-size: 11px; color: #333;")

        self.label_temp = QLabel("Temperatura: —")
        self.label_temp.setStyleSheet("font-size: 11px; color: #444;")

        self.label_method = QLabel("Metoda: —")
        self.label_method.setStyleSheet("font-size: 11px; color: #555;")

        top_bar.addWidget(self.btn)
        top_bar.addWidget(self.label_coords)
        top_bar.addWidget(self.label_temp)
        top_bar.addWidget(self.label_method)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # Web preglednik za kartu
        self.view = QWebEngineView()
        layout.addWidget(self.view, stretch=1)

        self.ucitaj_praznu_kartu()

    def ucitaj_praznu_kartu(self):
        mapa = folium.Map(location=[0, 0], zoom_start=2)
        mapa.save("moja_lokacija.html")
        self.view.load(QUrl.fromLocalFile(os.path.abspath("moja_lokacija.html")))

    def prikazi_lokaciju(self):
        lat, lon, opis, metoda = get_location()
        temp = get_temperature(lat, lon)

        self.label_coords.setText(f"Koordinate: {lat:.6f}, {lon:.6f}")
        self.label_method.setText(f"Metoda: {metoda}")
        self.label_temp.setText(
            f"Temperatura: {temp}°C" if temp is not None else "Temperatura: N/A"
        )

        # Kreiraj kartu
        mapa = folium.Map(location=[lat, lon], zoom_start=13)
        popup_text = f"{opis}<br>({lat:.6f}, {lon:.6f})"
        if temp is not None:
            popup_text += f"<br>🌡️ {temp} °C"

        folium.Marker(
            [lat, lon],
            popup=popup_text,
            tooltip="Tvoja lokacija"
        ).add_to(mapa)

        mapa.save("moja_lokacija.html")
        self.view.load(QUrl.fromLocalFile(os.path.abspath("moja_lokacija.html")))

        if "offline" in metoda.lower():
            QMessageBox.warning(self, "Upozorenje", "Nema interneta — prikazana je slučajna lokacija.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPSApp()
    window.show()
    sys.exit(app.exec_())
