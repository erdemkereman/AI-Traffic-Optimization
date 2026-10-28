import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)

traffic_data = []

for day in range(30):
    day_of_week = day % 7

    for hour in range(24):

        # Saate göre trafik yoğunluğu
        if 7 <= hour <= 9:
            main_lam = 30
            side_lam = 15
        elif 17 <= hour <= 19:
            main_lam = 35
            side_lam = 20
        elif 0 <= hour <= 5:
            main_lam = 5
            side_lam = 3
        else:
            main_lam = 15
            side_lam = 8

        # Hafta sonu etkisi
        if day_of_week >= 5:
            main_lam *= 0.75
            side_lam *= 0.85

        # Hava durumu
        weather = rng.choice(
            ["Clear", "Rainy"],
            p=[0.8, 0.2]
        )

        # Kaza ve etkinlik
        accident = bool(rng.random() < 0.05)
        event_intensity = round(float(rng.random()), 2)

        # Ana yol ve yan yol araç sayıları
        main_vehicles = int(rng.poisson(main_lam))
        side_vehicles = int(rng.poisson(side_lam))

        traffic_data.append({
            "scenario_id": len(traffic_data) + 1,
            "hour": hour,
            "day_of_week": day_of_week,
            "weather": weather,
            "accident": accident,
            "event_intensity": event_intensity,
            "main_road_vehicles": main_vehicles,
            "side_road_vehicles": side_vehicles
        })

df = pd.DataFrame(traffic_data)

project_root = Path(__file__).resolve().parents[2]

output_dir = project_root / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "traffic_scenarios.csv"

df.to_csv(output_file, index=False)

print("CSV kaydedildi:", output_file)

print(df.head())
print("Toplam senaryo:", len(df))