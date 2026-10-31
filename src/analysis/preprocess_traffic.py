from pathlib import Path
import pandas as pd

# Projenin ana klasorunu buluyoruz
project_root = Path(__file__).resolve().parents[2]

# Ham trafik verisinin dosya yolu
input_file = project_root / "data" / "raw" / "traffic_scenarios.csv"

# CSV dosyasini okuyoruz
df = pd.read_csv(input_file)

# Veri setinin genel bilgileri
print("Toplam satir ve sutun:", df.shape)

print("\nIlk 5 kayit:")
print(df.head())

print("\nVeri tipleri:")
print(df.dtypes)

print("\nEksik deger sayilari:")
print(df.isnull().sum())

print("\nTekrar eden satir sayisi:")
print(df.duplicated().sum())


# Veri araliklarini kontrol ediyoruz

invalid_hours = ~df["hour"].between(0, 23)

invalid_days = ~df["day_of_week"].between(0, 6)

invalid_events = ~df["event_intensity"].between(0, 1)

invalid_main = df["main_road_vehicles"] < 0

invalid_side = df["side_road_vehicles"] < 0

invalid_weather = ~df["weather"].isin(["Clear", "Rainy"])

print("\nGecersiz saat:", invalid_hours.sum())
print("Gecersiz gun:", invalid_days.sum())
print("Gecersiz etkinlik yogunlugu:", invalid_events.sum())
print("Gecersiz ana yol arac sayisi:", invalid_main.sum())
print("Gecersiz yan yol arac sayisi:", invalid_side.sum())
print("Gecersiz hava durumu:", invalid_weather.sum())
print("Tekrar eden senaryo ID:", df["scenario_id"].duplicated().sum())


# 1. Hava durumunu sayisal degere donusturuyoruz
df["weather"] = df["weather"].map({
    "Clear": 0,
    "Rainy": 1
})

# 2. Kaza bilgisini 0 ve 1 olarak sakliyoruz
df["accident"] = df["accident"].astype(int)

# 3. Toplam arac sayisini hesapliyoruz
df["total_vehicles"] = (
    df["main_road_vehicles"] + df["side_road_vehicles"]
)

# 4. Temizlenmis veriyi kaydediyoruz
output_file = project_root / "data" / "processed" / "traffic_cleaned.csv"

output_file.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_file, index=False)

print("\nTemizlenmis veri seti:")
print(df.head())

print("\nToplam kayit:", len(df))
print("Temizlenmis CSV:", output_file)