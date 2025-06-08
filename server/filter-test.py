import folium
import numpy as np
import os
import json
from filterpy.kalman import KalmanFilter
from datetime import datetime

# Veriyi oku
veriler = []
for file in os.listdir("devices/locationCache/d41d8cd98f00b204e9800998ecf8427e/"):
    if file.endswith(".json"):
        with open("devices/locationCache/d41d8cd98f00b204e9800998ecf8427e/" + file, "r") as f:
            data = json.load(f)
            veriler.append(data)

# Tarihe göre sırala (gerekirse)
veriler.sort(key=lambda x: x["timestamp"])

# Kalman filtresi
def kalman_filtrele(veriler):
    kf = KalmanFilter(dim_x=4, dim_z=2)
    dt = 1.0

    ilk_lat = veriler[0]["location"]["latitude"]
    ilk_lon = veriler[0]["location"]["longitude"]

    kf.x = np.array([ilk_lat, 0, ilk_lon, 0])
    kf.F = np.array([[1, dt, 0,  0],
                     [0, 1,  0,  0],
                     [0, 0,  1, dt],
                     [0, 0,  0, 1]])
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0]])
    kf.P *= 1000
    kf.R *= 0.0001
    kf.Q *= 0.01

    sonuc = []
    for v in veriler:
        z = np.array([v["location"]["latitude"], v["location"]["longitude"]])
        kf.predict()
        kf.update(z)
        sonuc.append({
            "timestamp": v["timestamp"],
            "location": {
                "latitude": float(kf.x[0]),
                "longitude": float(kf.x[2])
            }
        })
    return sonuc

def saniye_ortalama(veriler, window_second=10):
    sonuc = []
    pencere = []
    for i in range(len(veriler)):
        if len(pencere) > 0:
            if abs(pencere[0]["timestamp"] - veriler[i]["timestamp"]) < window_second:
                pencere.append(veriler[i])
            else:

                ort_time = sum(p["timestamp"] for p in pencere) / len(pencere)
                ort_lat = sum(p["location"]["latitude"] for p in pencere) / len(pencere)
                ort_lon = sum(p["location"]["longitude"] for p in pencere) / len(pencere)

                sonuc.append({
                    "type": "average",
                    "timestamp": ort_time,
                    "location": {"latitude": ort_lat, "longitude": ort_lon}
                })

                pencere = []
        elif len(pencere) == 0:
            pencere.append(veriler[i])
        
    return sonuc

def saniye_ortalama_kalman(veriler, window_second=10):
    sonuc = []
    pencere = []
    for i in range(len(veriler)):
        if len(pencere) > 0:
            if abs(pencere[0]["timestamp"] - veriler[i]["timestamp"]) < window_second:
                pencere.append(veriler[i])
            else:

                kf = KalmanFilter(dim_x=4, dim_z=2)
                dt = 1.0

                ilk_lat = pencere[0]["location"]["latitude"]
                ilk_lon = pencere[0]["location"]["longitude"]

                kf.x = np.array([ilk_lat, 0, ilk_lon, 0])
                kf.F = np.array([[1, dt, 0,  0],
                                [0, 1,  0,  0],
                                [0, 0,  1, dt],
                                [0, 0,  0, 1]])
                kf.H = np.array([[1, 0, 0, 0],
                                [0, 0, 1, 0]])
                kf.P *= 50
                kf.R *= 0.1
                kf.Q *= 0.01

                for v in pencere:
                    z = np.array([v["location"]["latitude"], v["location"]["longitude"]])
                    kf.predict()
                    kf.update(z)

                    sonuc.append({
                        "type": "kalman",
                        "timestamp": v["timestamp"],
                        "location": {
                            "latitude": float(kf.x[0]),
                            "longitude": float(kf.x[2])
                        }
                    })

                sonuc.append(veriler[i])

                pencere = []
        elif len(pencere) == 0:
            pencere.append(veriler[i])
        
    return sonuc

# Filtreler
veri_kalman = kalman_filtrele(veriler)
veri_pencere = saniye_ortalama(veriler, 10)
veri_pencere_kalman = saniye_ortalama_kalman(veri_pencere, 300)
veri_pencere_kalman_test = saniye_ortalama_kalman(veri_pencere_kalman, 300)
veri_pencere_kalman_test = saniye_ortalama_kalman(veri_pencere_kalman_test, 300)

# Haritanın merkezi
center_lat = sum(v["location"]["latitude"] for v in veriler) / len(veriler)
center_lon = sum(v["location"]["longitude"] for v in veriler) / len(veriler)
m = folium.Map(location=[center_lat, center_lon], zoom_start=17)

# Yardımcı çizim fonksiyonu
def rota_ciz(veri, color, label):
    coords = [(v["location"]["latitude"], v["location"]["longitude"]) for v in veri]
    folium.PolyLine(coords, color=color, weight=5, opacity=0.7, tooltip=label).add_to(m)
    for i, point in enumerate(coords):
        data = veri[i]
        #turn timestamp human readable
        date = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        folium.CircleMarker(point, radius=3, color=color, fill=True, fill_color=color,
                            tooltip=f"{label} #{i+1} \n{date} \n{data["type"]} \n{datetime.fromtimestamp(data["datePublished"] / 1000).strftime("%Y-%m-%d %H:%M:%S") if "datePublished" in data.keys() else ""} \n {str(data["location"]["accuracy"]) if "accuracy" in data["location"].keys() else ""}").add_to(m)

# Çizim
rota_ciz(veriler, "red", "Orijinal")
#rota_ciz(veri_pencere_kalman, "blue", "Kalman")
#rota_ciz(veri_pencere_kalman_test, "yellow", "Kalman-Test")

# Kaydet
m.save("harita_kalman_ortalama.html")