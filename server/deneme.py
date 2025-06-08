import json
import os
import math
import folium
from datetime import datetime

METERS_PER_DEGREE_LAT = 111320.0
def haversine(lat1, lon1, lat2, lon2):
    # Dünya yarıçapı (metre cinsinden)
    R = 6371000  
    # Radyana çevir
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # mesafe (metre)

def circleIntersection(lat1, lon1, r1, lat2, lon2, r2):
    d = haversine(lat1, lon1, lat2, lon2)
    return abs(r1 - r2) < d < (r1 + r2)

def intersectionRadius(lat1, lon1, r1, lat2, lon2, r2):
    d = haversine(lat1, lon1, lat2, lon2)
    if abs(r1 - r2) < d < (r1 + r2):
        return (r1 + r2 - d) / 2
    else:
        return 0

def geo_midpoint(lat1, lon1, lat2, lon2):
    # Radyana çevir
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Kartezyen koordinatlar
    x1 = math.cos(lat1) * math.cos(lon1)
    y1 = math.cos(lat1) * math.sin(lon1)
    z1 = math.sin(lat1)

    x2 = math.cos(lat2) * math.cos(lon2)
    y2 = math.cos(lat2) * math.sin(lon2)
    z2 = math.sin(lat2)

    # Ortalama al
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    z = (z1 + z2) / 2

    # Geri enlem-boylam
    lon = math.atan2(y, x)
    hyp = math.sqrt(x * x + y * y)
    lat = math.atan2(z, hyp)

    # Dereceye çevir
    return math.degrees(lat), math.degrees(lon)

def geo_midpoint_weighted(lat1, lon1, weight1, lat2, lon2, weight2):
    # Radyana çevir
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Kartezyen koordinatlar
    x1 = math.cos(lat1) * math.cos(lon1)
    y1 = math.cos(lat1) * math.sin(lon1)
    z1 = math.sin(lat1)

    x2 = math.cos(lat2) * math.cos(lon2)
    y2 = math.cos(lat2) * math.sin(lon2)
    z2 = math.sin(lat2)

    # Ağırlıklı ortalama
    total_weight = weight1 + weight2
    x = (x1 * weight1 + x2 * weight2) / total_weight
    y = (y1 * weight1 + y2 * weight2) / total_weight
    z = (z1 * weight1 + z2 * weight2) / total_weight

    # Geri dönüş (lat, lon)
    lon = math.atan2(y, x)
    hyp = math.sqrt(x * x + y * y)
    lat = math.atan2(z, hyp)

    return math.degrees(lat), math.degrees(lon)

def geo_midpoint_multiple(latitudes, longitudes):
    # Radyana çevir
    latitudes = [math.radians(lat) for lat in latitudes]
    longitudes = [math.radians(lon) for lon in longitudes]
    # Kartezyen koordinatlar
    x = sum(math.cos(lat) * math.cos(lon) for lat, lon in zip(latitudes, longitudes)) / len(latitudes)
    y = sum(math.cos(lat) * math.sin(lon) for lat, lon in zip(latitudes, longitudes)) / len(latitudes)
    z = sum(math.sin(lat) for lat in latitudes) / len(latitudes)
    # Geri dönüş (lat, lon)
    lon = math.atan2(y, x)
    hyp = math.sqrt(x * x + y * y)
    lat = math.atan2(z, hyp)
    return math.degrees(lat), math.degrees(lon)

def degrees_to_radians(degrees: float) -> float:
    """
    Dereceyi radyana çevirir.
    
    Args:
        degrees (float): Derece cinsinden açı.
        
    Returns:
        float: Radyan cinsinden açı.
    """
    return degrees * (math.pi / 180)

def point_to_point_distance_cartesian(p1_x: float, p1_y: float, p2_x: float, p2_y: float) -> float:
    """
    İki 2D nokta arasındaki Kartezyen mesafeyi hesaplar.
    
    Args:
        p1_x (float): Birinci noktanın X koordinatı.
        p1_y (float): Birinci noktanın Y koordinatı.
        p2_x (float): İkinci noktanın X koordinatı.
        p2_y (float): İkinci noktanın Y koordinatı.
        
    Returns:
        float: İki nokta arasındaki mesafe.
    """
    return math.sqrt((p1_x - p2_x)**2 + (p1_y - p2_y)**2)

def convert_cartesian_to_lat_lon(
    cartesian_points: list[tuple[float, float]],
    center_lat: float, center_lon: float,
    meters_per_degree_lat: float, meters_per_degree_lon: float
) -> list[tuple[float, float]]:
    """
    Lokal Kartezyen koordinatları enlem/boylam koordinatlarına geri dönüştürür.
    
    Args:
        cartesian_points (list[tuple[float, float]]): (x, y) koordinatlarının listesi.
        center_lat (float): Daire merkezinin orijinal enlemi.
        center_lon (float): Daire merkezinin orijinal boylamı.
        meters_per_degree_lat (float): Enlem derecesi başına metre.
        meters_per_degree_lon (float): Boylam derecesi başına metre (ortalama enleme göre).
        
    Returns:
        list[tuple[float, float]]: Dönüştürülmüş [(enlem, boylam), ...] listesi.
    """
    lat_lon_points = []
    for x, y in cartesian_points:
        ilat = center_lat + y / meters_per_degree_lat
        ilon = center_lon + x / meters_per_degree_lon
        lat_lon_points.append((ilat, ilon))
    return lat_lon_points

def line_circle_segment_intersection(
    lat1: float, lon1: float,
    lat2: float, lon2: float,
    center_lat: float, center_lon: float,
    radius_meters: float
) -> list[tuple[float, float]]:
    
    # Kayan nokta hassasiyeti için küçük bir tolerans değeri
    epsilon = 1e-9

    # --- Coğrafi koordinatları daire merkezine göre yerel Kartezyen koordinatlara dönüştürme ---
    # Bu dönüşüm, Dünya'nın küreselliğini basitleştirerek düz bir yüzey gibi davranır.
    # Küçük coğrafi alanlar için yeterince doğrudur.
    
    # Ortalama enlemi kullanarak boylam dönüşüm faktörünü hesapla
    # Bu, boylam derecesi başına metre değerinin, kullanılan enleme göre değiştiğini hesaba katar.
    avg_lat_rad = degrees_to_radians((lat1 + lat2 + center_lat) / 3.0)
    
    # Boylam derecesi başına metre (ortalama enleme göre)
    METERS_PER_DEGREE_LON = METERS_PER_DEGREE_LAT * math.cos(avg_lat_rad)

    # Noktaları daire merkezine göre Kartezyen koordinatlara dönüştür.
    # Daire merkezi (0,0) noktasına eşlenir.
    cx, cy = 0.0, 0.0 # Daire merkezi yerel Kartezyen koordinatlarda (0,0)
    
    p1_x = (lon1 - center_lon) * METERS_PER_DEGREE_LON
    p1_y = (lat1 - center_lat) * METERS_PER_DEGREE_LAT

    p2_x = (lon2 - center_lon) * METERS_PER_DEGREE_LON
    p2_y = (lat2 - center_lat) * METERS_PER_DEGREE_LAT

    # Segmentin başlangıç ve bitiş noktaları yerel Kartezyen koordinatlarda
    P1 = (p1_x, p1_y)
    P2 = (p2_x, p2_y)

    # Kesişim noktalarını depolayacak liste (önce Kartezyen, sonra Lat/Lon'a dönüştürülecek)
    raw_intersection_points = []
    
    # --- Dejenere Segment Durumu (P1 == P2) ---
    # Eğer segment tek bir noktaysa, bu noktanın dairenin çevresinde olup olmadığını kontrol et
    if abs(p1_x - p2_x) < epsilon and abs(p1_y - p2_y) < epsilon:
        dist_p1_to_c = point_to_point_distance_cartesian(P1[0], P1[1], cx, cy)
        if abs(dist_p1_to_c - radius_meters) < epsilon:
            # Tek nokta tam olarak dairenin çevresindeyse, bir kesişim var
            raw_intersection_points.append(P1)
        # Kesişim noktalarını Lat/Lon'a dönüştür ve döndür
        final_lat_lon_points = convert_cartesian_to_lat_lon(
            raw_intersection_points, 
            center_lat, center_lon, 
            METERS_PER_DEGREE_LAT, METERS_PER_DEGREE_LON
        )
        return final_lat_lon_points

    # --- Çizgi-Daire Kesişimi (Genel Durum) ---
    # Segmenti temsil eden vektör: D = P2 - P1
    dx, dy = p2_x - p1_x, p2_y - p1_y
    
    # Daire merkezinden P1'e vektör: F = P1 - C (C (0,0) olduğu için F = P1)
    fx, fy = p1_x - cx, p1_y - cy

    # Kuadratik denklem katsayıları: a*t^2 + b*t + c = 0
    # Burada 't', çizgi üzerindeki parametrik konumdur (P1'den P2'ye gittikçe t 0'dan 1'e değişir)
    a = dx*dx + dy*dy
    b = 2 * (fx*dx + fy*dy)
    c = (fx*fx + fy*fy) - radius_meters**2

    discriminant = b*b - 4*a*c

    if discriminant < 0:
        # Gerçek kök yok, yani sonsuz çizgi daireyi kesmiyor
        return []

    # Sonsuz çizgi üzerindeki kesişim noktaları için 't' değerlerini hesapla
    t_values = []
    if abs(discriminant) < epsilon: # Bir kök (teğet)
        t_values.append(-b / (2 * a))
    else: # İki farklı kök
        sqrt_discriminant = math.sqrt(discriminant)
        t_values.append((-b - sqrt_discriminant) / (2 * a))
        t_values.append((-b + sqrt_discriminant) / (2 * a))
    
    # 't' değerlerini filtreleyerek kesişim noktalarının segment [0, 1] aralığında olup olmadığını kontrol et
    for t in t_values:
        # epsilon kullanarak kapsayıcı karşılaştırma
        if t >= 0.0 - epsilon and t <= 1.0 + epsilon:
            # Kesişim noktasının Kartezyen (x, y) koordinatlarını hesapla
            ix = p1_x + t * dx
            iy = p1_y + t * dy
            
            # Kayan nokta hassasiyetinden dolayı noktanın gerçekten daire çevresinde olduğundan emin ol
            dist_to_center = point_to_point_distance_cartesian(ix, iy, cx, cy)
            if abs(dist_to_center - radius_meters) < epsilon:
                raw_intersection_points.append((ix, iy))
            
    # Aynı noktaların birden fazla kez eklenmesini önlemek için benzersizleştirme
    # Kayan nokta hassasiyeti nedeniyle çok yakın noktaları aynı kabul etmek için yuvarlama kullanırız.
    unique_intersection_points = []
    seen_points_quantized = set() # Yuvarlanmış noktaları depolamak için küme
    for p in raw_intersection_points:
        # Noktaları belirli bir ondalık basamağa yuvarla (örn. 6 basamak)
        quantized_p = (round(p[0], 6), round(p[1], 6)) 
        if quantized_p not in seen_points_quantized:
            seen_points_quantized.add(quantized_p)
            unique_intersection_points.append(p)
    
    # Benzersiz Kartezyen kesişim noktalarını Enlem/Boylam'a dönüştür
    final_lat_lon_points = convert_cartesian_to_lat_lon(
        unique_intersection_points, 
        center_lat, center_lon, 
        METERS_PER_DEGREE_LAT, METERS_PER_DEGREE_LON
    )

    # Enlem ve ardından boylam bazında sıralama yap (tutarlılık için)
    final_lat_lon_points.sort(key=lambda p: (p[0], p[1]))

    return final_lat_lon_points

# Veriyi oku
veriler = []
for file in os.listdir("devices/locationCache/d41d8cd98f00b204e9800998ecf8427e/"):
    if file.endswith(".json"):
        with open("devices/locationCache/d41d8cd98f00b204e9800998ecf8427e/" + file, "r") as f:
            data = json.load(f)
            veriler.append(data)

veriler.sort(key=lambda x: x["timestamp"])

timestamps = {}
for veri in veriler:
    if veri["timestamp"] not in timestamps:
        timestamps[veri["timestamp"]] = [veri]
    else:
        timestamps[veri["timestamp"]] = [*timestamps[veri["timestamp"]], veri]

        
for timestamp in timestamps:
    data = timestamps.get(timestamp)

    if len(data) > 1:
        #weighted average calculation
        ortalama_lat = sum(veri["location"]["latitude"] * veri["location"]["accuracy"] for veri in data) / sum(veri["location"]["accuracy"] for veri in data)
        ortalama_lon = sum(veri["location"]["longitude"] * veri["location"]["accuracy"] for veri in data) / sum(veri["location"]["accuracy"] for veri in data)
        ortalama_acc = sum(veri["location"]["accuracy"] for veri in data) / len(data)      

        timestamps[timestamp] = data[0] | {
            "location": {
                "latitude": ortalama_lat,
                "longitude": ortalama_lon,
                "accuracy": ortalama_acc
            }
        }
    elif len(data) == 1:
        timestamps[timestamp] = data[0]

timestamps = list(timestamps.values())
timestamps.sort(key=lambda x: x["timestamp"])

dots = {}

last_timestamp = None

for index, data in enumerate(timestamps):
    timestamp = timestamps[index]["timestamp"]

    if last_timestamp is None:
        dots[timestamp] = {
            "type": "start",
            "location": {
                "latitude": data["location"]["latitude"],
                "longitude": data["location"]["longitude"],
                "accuracy": data["location"]["accuracy"]
            }
        }

        veriler[index]["why"] = "start element"

        last_timestamp = timestamp
    else:
        last_data = dots.get(last_timestamp)
        
        intersect = circleIntersection(data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"], last_data["location"]["latitude"], last_data["location"]["longitude"], last_data["location"]["accuracy"])
        if intersect is True:
            intersect_timestamp = timestamp #int((timestamp + last_timestamp) / 2) #KONTOL ET
            intersect_radius = intersectionRadius(data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"], last_data["location"]["latitude"], last_data["location"]["longitude"], last_data["location"]["accuracy"])

            intersect_lat, intersect_lon = geo_midpoint_weighted(data["location"]["latitude"], data["location"]["longitude"], last_data["location"]["accuracy"], last_data["location"]["latitude"], last_data["location"]["longitude"], last_data["location"]["accuracy"])

            dots[intersect_timestamp] = {
                "type": "intersect with previous",
                "location": {
                    "latitude": intersect_lat,
                    "longitude": intersect_lon,
                    "accuracy": intersect_radius
                }
            }

            veriler[index]["why"] = "intersect with previous"

            last_timestamp = intersect_timestamp
        else:
            if index != len(timestamps) - 1:
                next_data = timestamps[index + 1]
                next_intersect = circleIntersection(data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"], next_data["location"]["latitude"], next_data["location"]["longitude"], next_data["location"]["accuracy"])
                if next_intersect is True:
                    intersect_lat, intersect_lon = geo_midpoint_weighted(data["location"]["latitude"], data["location"]["longitude"], next_data["location"]["accuracy"], next_data["location"]["latitude"], next_data["location"]["longitude"], data["location"]["accuracy"])
                    intersect_radius = intersectionRadius(data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"], next_data["location"]["latitude"], next_data["location"]["longitude"], next_data["location"]["accuracy"])

                    circle_intersects = line_circle_segment_intersection(last_data["location"]["latitude"], last_data["location"]["longitude"], intersect_lat, intersect_lon, data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"])
                    
                    if len(circle_intersects) == 0:
                        midpoint_lat, midpoint_lon = geo_midpoint(last_data["location"]["latitude"], last_data["location"]["longitude"], intersect_lat, intersect_lon)

                        circle_intersects_midpoint = line_circle_segment_intersection(midpoint_lat, midpoint_lon, data["location"]["latitude"], data["location"]["longitude"], data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"])

                        

                        if len(circle_intersects_midpoint) == 1:
                            dots[timestamp] = {
                                "type": "intersect midpoint",
                                "location": {
                                    "latitude": circle_intersects_midpoint[0][0],
                                    "longitude": circle_intersects_midpoint[0][1],
                                    "accuracy": 1
                                }
                            }

                            veriler[index]["why"] = "intersect with next and circle intersect midpoint"

                            last_timestamp = timestamp
                        elif len(circle_intersects_midpoint) == 0:
                            

                            dots[timestamp] = {
                                "type": "intersect prev and next",
                                "location": {
                                    "latitude": midpoint_lat,
                                    "longitude": midpoint_lon,
                                    "accuracy": haversine(last_data["location"]["latitude"], last_data["location"]["longitude"], intersect_lat, intersect_lon) - last_data["location"]["accuracy"] - intersect_radius / 2
                                }
                            }

                            veriler[index]["why"] = "circle includes prev and next"

                            last_timestamp = timestamp
                        else:
                            print(data["location"])
                            print(midpoint_lat, midpoint_lon)
                            print(len(circle_intersects_midpoint))

                            print(f"line_circle_segment_intersection({midpoint_lat}, {midpoint_lon}, {data["location"]["latitude"]}, {data["location"]["longitude"]}, {data["location"]["latitude"]}, {data["location"]["longitude"]}, {data["location"]["accuracy"]})")
                    else:
                        latitudes = [circle_intersect[0] for circle_intersect in circle_intersects]
                        longitudes = [circle_intersect[1] for circle_intersect in circle_intersects]

                        circle_intersect_lat , circle_intersect_lon = geo_midpoint_multiple(latitudes, longitudes)
                        circle_intersect_acc = data["location"]["accuracy"] if len(circle_intersects) == 1 else haversine(latitudes[0], longitudes[0], latitudes[1], longitudes[1]) / 2

                        dots[timestamp] = {
                            "type": "intersect with next",
                            "location": {
                                "latitude": circle_intersect_lat,
                                "longitude": circle_intersect_lon,
                                "accuracy": circle_intersect_acc
                            }
                        }

                        veriler[index]["why"] = "circle intersects with next and midline intersacts with circle " + str(len(circle_intersects)) + " times"

                        last_timestamp = timestamp
                else:
                    circle_intersects = line_circle_segment_intersection(last_data["location"]["latitude"], last_data["location"]["longitude"], next_data["location"]["latitude"], next_data["location"]["longitude"], data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"])

                    if timestamp == 1749042656:
                        print(circle_intersects)

                    if len(circle_intersects) == 0:
                        midpoint_lat, midpoint_lon = geo_midpoint(last_data["location"]["latitude"], last_data["location"]["longitude"], next_data["location"]["latitude"], next_data["location"]["longitude"])

                        circle_intersects_midpoint = line_circle_segment_intersection(midpoint_lat, midpoint_lon, data["location"]["latitude"], data["location"]["longitude"], data["location"]["latitude"], data["location"]["longitude"], data["location"]["accuracy"])

                        if timestamp == 1749042656:
                            print(circle_intersects_midpoint)
                            print(last_data["location"])
                            print(data["location"])
                            print(next_data["location"])

                        if len(circle_intersects_midpoint) == 1:
                            dots[timestamp] = {
                                "type": "intersect midpoint",
                                "location": {
                                    "latitude": circle_intersects_midpoint[0][0],
                                    "longitude": circle_intersects_midpoint[0][1],
                                    "accuracy": 1
                                }
                            }

                            veriler[index]["why"] = "midpoint not intersect with circle"

                            last_timestamp = timestamp
                        elif len(circle_intersects_midpoint) == 0:
                            dots[timestamp] = {
                                "type": "intersect prev and next",
                                "location": {
                                    "latitude": midpoint_lat,
                                    "longitude": midpoint_lon,
                                    "accuracy": haversine(last_data["location"]["latitude"], last_data["location"]["longitude"], next_data["location"]["latitude"], next_data["location"]["longitude"]) - last_data["location"]["accuracy"] - next_data["location"]["accuracy"]
                                }
                            }

                            veriler[index]["why"] = "circles in midcircle midpoint not intersect with circle"
                            
                            last_timestamp = timestamp
                        else:
                            print(data["location"])

                    elif len(circle_intersects) == 1:
                        circle_intersect_lat, circle_intersect_lon = circle_intersects[0]
                        circle_intersect_acc = data["location"]["accuracy"]

                        dots[timestamp] = {
                            "type": "intersect",
                            "location": {
                                "latitude": circle_intersect_lat,
                                "longitude": circle_intersect_lon,
                                "accuracy": circle_intersect_acc
                            }
                        }

                        veriler[index]["why"] = "circle intersects with next and midline intersacts with circle " + str(len(circle_intersects)) + " times"

                        last_timestamp = timestamp
                    
                    else:
                        latitudes = [circle_intersect[0] for circle_intersect in circle_intersects]
                        longitudes = [circle_intersect[1] for circle_intersect in circle_intersects]

                        circle_intersect_lat , circle_intersect_lon = geo_midpoint_multiple(latitudes, longitudes)
                        circle_intersect_acc = haversine(latitudes[0], longitudes[0], latitudes[1], longitudes[1]) / 2

                        dots[timestamp] = {
                            "type": "intersect",
                            "location": {
                                "latitude": circle_intersect_lat,
                                "longitude": circle_intersect_lon,
                                "accuracy": circle_intersect_acc
                            }
                        }

                        veriler[index]["why"] = "intersect with circle " + str(len(circle_intersects)) + " times"
                        last_timestamp = timestamp
                        
            else:
                dots[timestamp] = {
                    "type": "normal",
                    "location": {
                        "latitude": data["location"]["latitude"],
                        "longitude": data["location"]["longitude"],
                        "accuracy": data["location"]["accuracy"]
                    }
                }

                veriler[index]["why"] = "last element"

                last_timestamp = timestamp
    if timestamp not in dots:
        print("kaçak var : ", timestamp)
            
center_lat = sum(dots[dot]["location"]["latitude"] for dot in dots) / len(dots)
center_lon = sum(dots[dot]["location"]["longitude"] for dot in dots) / len(dots)
m = folium.Map(location=[center_lat, center_lon], zoom_start=17)

print("konumlar : ", len(timestamps))
print("noktalar : ", len(dots))

i = 0
for data in timestamps:
    if data["timestamp"] not in dots:
        i += 1

print("noktalarda olmayan konumlar : ", i)

coords = []
circles = []

i = 0
for dot in dots:
    i += 1
    if i > 200:
        break
    point = (dots[dot]["location"]["latitude"], dots[dot]["location"]["longitude"])
    date = datetime.fromtimestamp(dot).strftime("%Y-%m-%d %H:%M:%S")
    coords.append(point)
    circles.append(folium.CircleMarker(point, radius=3, color="red", fill=True, fill_color="red",
                            tooltip=f"\n{date} \n{dots[dot]["type"]} { "<br>Accuracy : " + str(dots[dot]["location"]["accuracy"]) if "accuracy" in dots[dot]["location"].keys() else ""} <br> {point[0]}, {point[1]}"))

folium.PolyLine(coords, color="red", weight=5, opacity=0.7, tooltip="Deneme").add_to(m)

def rota_ciz(veri, color, label):
    coords = [(v["location"]["latitude"], v["location"]["longitude"]) for v in veri]
    #folium.PolyLine(coords, color=color, weight=5, opacity=0.7, tooltip=label).add_to(m)
    for i, point in enumerate(coords):
        data = veri[i]
        if data["timestamp"] in dots:
            folium.PolyLine([point, (dots[data["timestamp"]]["location"]["latitude"], dots[data["timestamp"]]["location"]["longitude"])], color="green", weight=4, opacity=0.5).add_to(m)
        date = datetime.fromtimestamp(data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        folium.Circle(point, radius=data["location"]["accuracy"], color="yellow", fill=False, opacity=0.5).add_to(m)
        folium.CircleMarker(point, radius=3, color=color, fill=True, fill_color=color,
                            tooltip=f"{data["why"] if "why" in data.keys() else "i dunno?"} <br> {label} #{i+1} \n{date} \n{data["type"]} \n{datetime.fromtimestamp(data["datePublished"] / 1000).strftime("%Y-%m-%d %H:%M:%S") if "datePublished" in data.keys() else ""} \n {str(data["location"]["accuracy"]) if "accuracy" in data["location"].keys() else ""}").add_to(m)

# Çizim
rota_ciz(veriler[:200], "blue", "Orijinal")

for circle in circles:
    circle.add_to(m)

m.save("deneme.html")