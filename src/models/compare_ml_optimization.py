
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.simulation.wait_time_simulator import simulate_average_wait
from src.simulation.traffic_simulator import find_best_green_time


# 1. Dosya yollari
project_root = Path(__file__).resolve().parents[2]

data_file = (
    project_root / "data" / "processed" /
    "traffic_cleaned.csv"
)

model_file = (
    project_root / "results" / "models" /
    "random_forest_optimizer.joblib"
)

output_file = (
    project_root / "data" / "processed" /
    "ml_optimization_results.csv"
)


# 2. Verileri ve modeli yukle
df = pd.read_csv(data_file)
bundle = joblib.load(model_file)

model = bundle["model"]
feature_columns = bundle["feature_columns"]

test_scenarios = set(bundle["test_scenarios"])

# Yalnizca egitimde gorulmemis senaryolari kullan
df = df[df["scenario_id"].isin(test_scenarios)].copy()

assert len(df) == 144

results = []


# 3. Her test senaryosunu degerlendir
for _, row in df.iterrows():

    main_vehicles = int(row["main_road_vehicles"])
    side_vehicles = int(row["side_road_vehicles"])

    weather = "Rainy" if row["weather"] == 1 else "Clear"
    accident = bool(row["accident"])

    # A. Sabit sinyalizasyon
    fixed_wait = simulate_average_wait(
        main_vehicles,
        side_vehicles,
        27,
        27,
        weather,
        accident
    )

    # B. Kuyruk odakli adaptif sinyalizasyon
    best_queue_plan = find_best_green_time(
        main_vehicles,
        side_vehicles,
        weather,
        accident
    )

    # Fonksiyonun dondurdugu plan bilgisi
    # main_green ve side_green anahtarlarini kullaniyoruz
    adaptive_main = best_queue_plan["main_green"]
    adaptive_side = best_queue_plan["side_green"]

    adaptive_wait = simulate_average_wait(
        main_vehicles,
        side_vehicles,
        adaptive_main,
        adaptive_side,
        weather,
        accident
    )

    # C. ML icin 35 aday yesil planini olustur
    candidates = []

    for main_green in range(10, 45):
        side_green = 54 - main_green

        candidates.append({
            "hour": int(row["hour"]),
            "day_of_week": int(row["day_of_week"]),
            "weather": int(row["weather"]),
            "accident": int(row["accident"]),
            "event_intensity": float(row["event_intensity"]),
            "main_road_vehicles": main_vehicles,
            "side_road_vehicles": side_vehicles,
            "main_green": main_green,
            "side_green": side_green
        })

    candidate_df = pd.DataFrame(candidates)

    # ML tahminleri
    predictions = model.predict(
        candidate_df[feature_columns]
    )

    best_ml_index = int(np.argmin(predictions))
    best_ml_plan = candidate_df.iloc[best_ml_index]

    ml_main = int(best_ml_plan["main_green"])
    ml_side = int(best_ml_plan["side_green"])

    # ML planinin simulatordeki gercek hedef degeri
    ml_wait = simulate_average_wait(
        main_vehicles,
        side_vehicles,
        ml_main,
        ml_side,
        weather,
        accident
    )

    # D. Simulatore gore gercek minimum bekleme
    actual_waits = []

    for main_green in range(10, 45):
        side_green = 54 - main_green

        wait = simulate_average_wait(
            main_vehicles,
            side_vehicles,
            main_green,
            side_green,
            weather,
            accident
        )

        actual_waits.append(wait)

    optimal_wait = min(actual_waits)

    results.append({
        "scenario_id": int(row["scenario_id"]),
        "fixed_wait": fixed_wait,
        "adaptive_wait": adaptive_wait,
        "ml_wait": ml_wait,
        "optimal_wait": optimal_wait,
        "ml_main_green": ml_main,
        "ml_side_green": ml_side
    })


# 4. Sonuclari kaydet
results_df = pd.DataFrame(results)

output_file.parent.mkdir(parents=True, exist_ok=True)
results_df.to_csv(output_file, index=False)


# 5. Ortalama bekleme sureleri
fixed_mean = results_df["fixed_wait"].mean()
adaptive_mean = results_df["adaptive_wait"].mean()
ml_mean = results_df["ml_wait"].mean()
optimal_mean = results_df["optimal_wait"].mean()


def improvement(baseline, candidate):
    if baseline == 0:
        return 0.0
    return (baseline - candidate) / baseline * 100


print("\nTRF-008 OPTIMIZASYON KARSILASTIRMASI")
print("Test senaryosu:", len(results_df))

print("\nORTALAMA BEKLEME SURELERI")
print("Sabit:", round(fixed_mean, 3), "sn")
print("Adaptif:", round(adaptive_mean, 3), "sn")
print("ML:", round(ml_mean, 3), "sn")
print("Teorik optimum:", round(optimal_mean, 3), "sn")

print("\nSABIT SISTEME GORE IYILESME")
print(
    "Adaptif:",
    round(improvement(fixed_mean, adaptive_mean), 2),
    "%"
)
print(
    "ML:",
    round(improvement(fixed_mean, ml_mean), 2),
    "%"
)

print("\nML OPTIMALDEN NE KADAR UZAK?")
print(
    "Ortalama fark:",
    round(ml_mean - optimal_mean, 3),
    "sn"
)

print("\nILK 10 SONUC")
print(results_df.head(10))

print("\nDosya kaydedildi:", output_file)
