
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. VERI SETINI OKUMA
# ==========================================

project_root = Path(__file__).resolve().parents[2]

input_file = project_root / "data" / "processed" / "traffic_cleaned.csv"

df = pd.read_csv(input_file)


# ==========================================
# 2. TEMEL TRAFIK ISTATISTIKLERI
# ==========================================

print("Toplam senaryo:", len(df))

print("\nOrtalama arac sayisi:")
print(df["total_vehicles"].mean())

print("\nMinimum arac sayisi:")
print(df["total_vehicles"].min())

print("\nMaksimum arac sayisi:")
print(df["total_vehicles"].max())


# ==========================================
# 3. SAATLERE GORE TRAFIK ANALIZI
# ==========================================

hourly_traffic = df.groupby("hour")["total_vehicles"].mean()

print("\nSaatlere gore ortalama trafik:")
print(hourly_traffic)


# ==========================================
# 4. HAFTA ICI / HAFTA SONU ANALIZI
# ==========================================

df["day_type"] = df["day_of_week"].apply(
    lambda day: "Hafta Ici" if day < 5 else "Hafta Sonu"
)

day_type_traffic = df.groupby("day_type")["total_vehicles"].mean()

print("\nHafta ici / hafta sonu ortalama trafik:")
print(day_type_traffic)


# ==========================================
# 5. HAVA DURUMUNA GORE TRAFIK ANALIZI
# ==========================================

# TRF-004'te Clear = 0, Rainy = 1 yapmistik.
weather_traffic = df.groupby("weather")["total_vehicles"].mean()

print("\nHava durumuna gore ortalama trafik:")
print(weather_traffic)


# ==========================================
# 6. GRAFIK KLASORUNU HAZIRLAMA
# ==========================================

output_dir = project_root / "results" / "figures"
output_dir.mkdir(parents=True, exist_ok=True)


# ==========================================
# 7. GRAFIK 1 - SAATLIK TRAFIK
# ==========================================

plt.figure(figsize=(12, 5))

plt.plot(
    hourly_traffic.index,
    hourly_traffic.values,
    marker="o"
)

plt.title("Saatlere Gore Ortalama Trafik Yogunlugu")
plt.xlabel("Saat")
plt.ylabel("Ortalama Arac Sayisi")
plt.xticks(range(24))
plt.grid(True)

plt.tight_layout()
plt.savefig(output_dir / "hourly_traffic.png")


# ==========================================
# 8. GRAFIK 2 - HAFTA ICI / HAFTA SONU
# ==========================================

plt.figure(figsize=(7, 5))

plt.bar(
    ["Hafta Ici", "Hafta Sonu"],
    [
        day_type_traffic.loc["Hafta Ici"],
        day_type_traffic.loc["Hafta Sonu"]
    ]
)

plt.title("Hafta Ici ve Hafta Sonu Trafik Karsilastirmasi")
plt.xlabel("Gun Tipi")
plt.ylabel("Ortalama Arac Sayisi")
plt.grid(axis="y")

plt.tight_layout()
plt.savefig(output_dir / "weekday_weekend_traffic.png")


# ==========================================
# 9. GRAFIK 3 - HAVA DURUMU
# ==========================================

plt.figure(figsize=(7, 5))

plt.bar(
    ["Acik", "Yagmurlu"],
    [
        weather_traffic.loc[0],
        weather_traffic.loc[1]
    ]
)

plt.title("Hava Durumuna Gore Ortalama Trafik")
plt.xlabel("Hava Durumu")
plt.ylabel("Ortalama Arac Sayisi")
plt.grid(axis="y")

plt.tight_layout()
plt.savefig(output_dir / "weather_traffic.png")


# ==========================================
# 10. GRAFIKLERI GOSTERME
# ==========================================

print("\nGrafikler kaydedildi:", output_dir)

plt.show()
