# gps_server_dynamic_map_zoom_threadsafe.py
import sys
import socket
import threading
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer, QUrl

HOST = '0.0.0.0'
PORT = 5000

class GPSServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPS Multi-Client Server - Thread-Safe Dynamic Map")
        self.setGeometry(50, 50, 1200, 800)

        self.clients = {}  # {client_name: {"path": [(lat, lon)], "last_update": datetime, "active": bool, "color": str}}
        self.lock = threading.Lock()

        # GUI
        self.client_container = QWidget()
        self.client_layout = QVBoxLayout()
        self.client_container.setLayout(self.client_layout)
        self.map_view = QWebEngineView()

        layout = QVBoxLayout()
        layout.addWidget(self.client_container)
        layout.addWidget(self.map_view, stretch=1)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize map HTML (Leaflet)
        self.init_map()

        # Start server thread
        threading.Thread(target=self.server_loop, daemon=True).start()

        # Timer to refresh map
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_map_js)
        self.timer.start(1000)  # update every second

    def init_map(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>GPS Dynamic Map</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                html, body, #map { height: 100%; margin: 0; padding: 0; }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map;
                var clientMarkers = {};
                var clientPaths = {};

                function initMap() {
                    map = L.map('map').setView([0, 0], 2);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        maxZoom: 19
                    }).addTo(map);
                }

                function updateClients(data_json) {
                    if (!map) return;
                    var data = JSON.parse(data_json);
                    for (const [cid, info] of Object.entries(data)) {
                        let path = info.path;
                        if (!path.length) continue;
                        let last = path[path.length - 1];
                        if (!clientMarkers[cid]) {
                            clientMarkers[cid] = L.marker(last).addTo(map).bindPopup(cid);
                            clientPaths[cid] = L.polyline(path, {color: info.color}).addTo(map);
                        } else {
                            clientMarkers[cid].setLatLng(last);
                            clientPaths[cid].setLatLngs(path);
                        }
                    }
                }

                function zoomToClient(cid) {
                    if (clientMarkers[cid]) {
                        map.setView(clientMarkers[cid].getLatLng(), 17);
                        clientMarkers[cid].openPopup();
                    }
                }

                document.addEventListener("DOMContentLoaded", initMap);
            </script>
        </body>
        </html>
        """
        self.map_view.setHtml(html, QUrl("about:blank"))

    def server_loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening on {HOST}:{PORT}")
            client_id = 0
            while True:
                conn, addr = s.accept()
                client_id += 1
                client_name = f"Client-{client_id}"
                print(f"{client_name} connected from {addr}")
                threading.Thread(target=self.handle_client, args=(conn, client_name), daemon=True).start()

    def handle_client(self, conn, client_name):
        with conn:
            with self.lock:
                self.clients[client_name] = {
                    "path": [],
                    "last_update": None,
                    "active": True,
                    "color": self.pick_color(client_name)
                }

            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    lat, lon = map(float, data.decode().split(','))
                    now = datetime.now()
                    with self.lock:
                        self.clients[client_name]["path"].append((lat, lon))
                        self.clients[client_name]["last_update"] = now
                        self.clients[client_name]["active"] = True
                    QTimer.singleShot(0, self.update_label)  # thread-safe
                except Exception as e:
                    print(f"{client_name} sent invalid data:", e)
                    break

            with self.lock:
                self.clients[client_name]["active"] = False
            print(f"{client_name} disconnected")
            QTimer.singleShot(0, self.update_label)  # thread-safe

    def pick_color(self, client_name):
        colors = ["red", "blue", "green", "purple", "orange", "darkred", "lightblue", "pink"]
        return colors[hash(client_name) % len(colors)]

    def update_label(self):
        # Clear current layout
        while self.client_layout.count():
            item = self.client_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        with self.lock:
            if self.clients:
                for cid, info in self.clients.items():
                    if info["path"]:
                        lat, lon = info["path"][-1]
                        ts = info["last_update"].strftime("%H:%M:%S") if info["last_update"] else "N/A"
                        status = "ACTIVE" if info["active"] else "DISCONNECTED"
                        line_widget = QWidget()
                        line_layout = QHBoxLayout()
                        line_layout.setContentsMargins(0, 0, 0, 0)

                        label = QLabel(f"{cid} [{status}]: Last ({lat:.5f}, {lon:.5f}) at {ts}")
                        btn = QPushButton("Zoom")
                        btn.clicked.connect(lambda _, c=cid: self.zoom_to_client(c))

                        line_layout.addWidget(label)
                        line_layout.addWidget(btn)
                        line_widget.setLayout(line_layout)
                        self.client_layout.addWidget(line_widget)
            else:
                self.client_layout.addWidget(QLabel("No clients connected."))

    def zoom_to_client(self, client_name):
        page = self.map_view.page()
        if page is None:
            print("Error: map_view.page() is None – page not loaded yet.")
            return

        js_code = f"zoomToClient('{client_name}');"
        #self.map_view.page().runJavaScript(js_code)
        page.runJavaScript(js_code)
        
    def refresh_map_js(self):
        with self.lock:
            if not self.clients:
                return
            # Convert datetime to string for JSON serialization
            serializable_clients = {}
            for cid, info in self.clients.items():
                serializable_clients[cid] = {
                    "path": info["path"],
                    "active": info["active"],
                    "color": info["color"],
                    "last_update": info["last_update"].strftime("%H:%M:%S") if info["last_update"] else None
                }

            data_to_send = json.dumps(serializable_clients)

        page = self.map_view.page()
        if page is None:
            print("Error: map_view.page() is None – page not loaded yet.")
            return

        js_code = f"updateClients('{data_to_send}');"
        #self.map_view.page().runJavaScript(js_code)
        page.runJavaScript(js_code)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPSServerApp()
    window.show()
    sys.exit(app.exec_())
