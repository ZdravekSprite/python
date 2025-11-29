import tkinter as tk
# pip install folium geocoder
import folium
import geocoder
import random
import webbrowser
import os

def get_location():
    """Vrati (lat, lon, metoda) tuple prema dostupnosti uređaja/interneta"""
    # 1. Pokušaj IP lokaciju
    try:
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            lat, lon = g.latlng
            return lat, lon, "IP geolokacija"
    except Exception as e:
        print("IP geolokacija nije uspjela:", e)

    # 2. Ako nema ni IP ni internet — random lokacija
    lat = random.uniform(-85, 85)
    lon = random.uniform(-180, 180)
    return lat, lon, "Slučajna lokacija (offline)"

def prikazi_lokaciju():
    lat, lon, metoda = get_location()

    # Ispis u GUI
    label_coords.config(text=f"Koordinate: {lat:.6f}, {lon:.6f}")
    label_metoda.config(text=f"Metoda: {metoda}")

    # Generiraj kartu
    mapa = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker(
        [lat, lon],
        popup=f"{metoda}\n({lat:.6f}, {lon:.6f})",
        tooltip="Tvoja lokacija"
    ).add_to(mapa)

    # Spremi kao HTML
    mapa_file = "moja_lokacija.html"
    mapa.save(mapa_file)

    # Otvori u pregledniku
    webbrowser.open('file://' + os.path.realpath(mapa_file))

# ----- GUI -----
root = tk.Tk()
root.title("GPS aplikacija (desktop)")
root.geometry("400x200")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True, fill="both")

button = tk.Button(frame, text="📍 Prikaži lokaciju", font=("Arial", 14), command=prikazi_lokaciju)
button.pack(pady=10)

label_coords = tk.Label(frame, text="Koordinate: —", font=("Arial", 12))
label_coords.pack()

label_metoda = tk.Label(frame, text="Metoda: —", font=("Arial", 12))
label_metoda.pack()

label_info = tk.Label(frame, text="Karta će se otvoriti u pregledniku", font=("Arial", 10), fg="gray")
label_info.pack(pady=10)

root.mainloop()
