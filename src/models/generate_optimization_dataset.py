
from pathlib import Path

import pandas as pd

from src.simulation.wait_time_simulator import simulate_average_wait


# 1. Dosya yollarini belirle
project_root = Path(__file__).resolve().parents[2]

input_file = project_root / "data" / "processed" / "traffic_cleaned.csv"

output_file = (
    project_root / "data" / "processed" /
    "optimization_dataset.csv"
)


# 2. Temizlenmis trafik verisini oku
df = pd.read_csv(input_file)

records = []


# 3. Her senaryo icin farkli yesil surelerini dene
for _, row in df.iterrows():

    weather = "Rainy" if row["weather"] == 1 else "Clear"

    accident = bool(row["accident"])

    main_vehicles = int(row["main_road_vehicles"])
    side_vehicles = int(row["side_road_vehicles"])

    # Ana yol 10-44 saniye arasinda olabilir
    for main_green in range(10, 45):

        side_green = 54 - main_green

        average_wait = simulate_average_wait(
            main_vehicles=main_vehicles,
            side_vehicles=side_vehicles,
            main_green=main_green,
            side_green=side_green,
            weather=weather,
            accident=accident
        )

        records.append({
            "scenario_id": int(row["scenario_id"]),
            "hour": int(row["hour"]),
            "day_of_week": int(row["day_of_week"]),
            "weather": int(row["weather"]),
            "accident": int(row["accident"]),
            "event_intensity": float(row["event_intensity"]),
            "main_road_vehicles": main_vehicles,
            "side_road_vehicles": side_vehicles,
            "main_green": main_green,
            "side_green": side_green,
            "average_wait_seconds": average_wait
        })


# 4. Yeni veri setini olustur
optimization_df = pd.DataFrame(records)


# 5. Veriyi kaydet
output_file.parent.mkdir(parents=True, exist_ok=True)

optimization_df.to_csv(output_file, index=False)


# 6. Sonuclari kontrol et
print("Orijinal senaryo sayisi:", len(df))
print("Toplam egitim kaydi:", len(optimization_df))

print("\nVeri seti boyutu:")
print(optimization_df.shape)

print("\nIlk 10 kayit:")
print(optimization_df.head(10))

print("\nBekleme suresi istatistikleri:")
print(optimization_df["average_wait_seconds"].describe())

print("\nDosya kaydedildi:", output_file)




from pathlib import Path

import pandas as pd

from src.simulation.wait_time_simulator import simulate_average_wait


# 1. Dosya yollarini belirle
project_root = Path(__file__).resolve().parents[2]

input_file = project_root / "data" / "processed" / "traffic_cleaned.csv"

output_file = (
    project_root / "data" / "processed" /
    "optimization_dataset.csv"
)


# 2. Temizlenmis trafik verisini oku
df = pd.read_csv(input_file)

records = []


# 3. Her senaryo icin farkli yesil surelerini dene
for _, row in df.iterrows():

    weather = "Rainy" if row["weather"] == 1 else "Clear"

    accident = bool(row["accident"])

    main_vehicles = int(row["main_road_vehicles"])
    side_vehicles = int(row["side_road_vehicles"])

    # Ana yol 10-44 saniye arasinda olabilir
    for main_green in range(10, 45):

        side_green = 54 - main_green

        average_wait = simulate_average_wait(
            main_vehicles=main_vehicles,
            side_vehicles=side_vehicles,
            main_green=main_green,
            side_green=side_green,
            weather=weather,
            accident=accident
        )

        records.append({
            "scenario_id": int(row["scenario_id"]),
            "hour": int(row["hour"]),
            "day_of_week": int(row["day_of_week"]),
            "weather": int(row["weather"]),
            "accident": int(row["accident"]),
            "event_intensity": float(row["event_intensity"]),
            "main_road_vehicles": main_vehicles,
            "side_road_vehicles": side_vehicles,
            "main_green": main_green,
            "side_green": side_green,
            "average_wait_seconds": average_wait
        })


# 4. Yeni veri setini olustur
optimization_df = pd.DataFrame(records)


# 5. Veriyi kaydet
output_file.parent.mkdir(parents=True, exist_ok=True)

optimization_df.to_csv(output_file, index=False)


# 6. Sonuclari kontrol et
print("Orijinal senaryo sayisi:", len(df))
print("Toplam egitim kaydi:", len(optimization_df))

print("\nVeri seti boyutu:")
print(optimization_df.shape)

print("\nIlk 10 kayit:")
print(optimization_df.head(10))

print("\nBekleme suresi istatistikleri:")
print(optimization_df["average_wait_seconds"].describe())

print("\nDosya kaydedildi:", output_file)
