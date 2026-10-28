from pathlib import Path

import pandas as pd

from traffic_simulator import simulate_intersection, find_best_green_time


project_root = Path(__file__).resolve().parents[2]

input_file = project_root / "data" / "raw" / "traffic_scenarios.csv"

df = pd.read_csv(input_file)

results = []

for _, row in df.iterrows():
    main_vehicles = int(row["main_road_vehicles"])
    side_vehicles = int(row["side_road_vehicles"])

    weather = row["weather"]
    accident = bool(row["accident"])

    fixed = simulate_intersection(
        main_vehicles=main_vehicles,
        side_vehicles=side_vehicles,
        main_green=27,
        side_green=27,
        weather=weather,
        accident=accident
    )

    adaptive = find_best_green_time(
        main_vehicles=main_vehicles,
        side_vehicles=side_vehicles,
        weather=weather,
        accident=accident
    )

    results.append({
        "scenario_id": int(row["scenario_id"]),
        "fixed_queue": fixed["total_queue"],
        "adaptive_queue": adaptive["total_queue"],
        "best_main_green": adaptive["main_green"],
        "best_side_green": adaptive["side_green"]
    })


results_df = pd.DataFrame(results)

print("Test edilen senaryo:", len(results_df))
print("Sabit sistem ortalama kuyruk:", results_df["fixed_queue"].mean())
print("Adaptif sistem ortalama kuyruk:", results_df["adaptive_queue"].mean())

output_file = project_root / "data" / "processed" / "simulation_results.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)

results_df.to_csv(output_file, index=False)

print("Sonuclar kaydedildi:", output_file)