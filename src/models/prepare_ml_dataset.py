from pathlib import Path
from src.simulation.wait_time_simulator import simulate_average_wait
import pandas as pd

project_root = Path(__file__).resolve().parents[2]

traffic_file = project_root / "data" / "processed" / "traffic_cleaned.csv"
simulation_file = project_root / "data" / "processed" / "simulation_results.csv"

traffic_df = pd.read_csv(traffic_file)
simulation_df = pd.read_csv(simulation_file)

# Ortak scenario_id uzerinden birlestir
df = pd.merge(
    traffic_df,
    simulation_df,
    on="scenario_id",
    how="inner",
    validate="one_to_one"
)

print("Trafik verisi:", traffic_df.shape)
print("Simulasyon verisi:", simulation_df.shape)
print("Birlestirilmis veri:", df.shape)

print("\nIlk 5 kayit:")
print(df.head())

print("\nSutunlar:")
print(df.columns.tolist())


# Hava durumu sayisal olarak tutuluyor.
# Simulasyon fonksiyonumuz ise "Clear" / "Rainy" bekliyor.

df["average_wait_seconds"] = df.apply(
    lambda row: simulate_average_wait(
        main_vehicles=int(row["main_road_vehicles"]),
        side_vehicles=int(row["side_road_vehicles"]),
        main_green=int(row["best_main_green"]),
        side_green=int(row["best_side_green"]),
        weather="Rainy" if row["weather"] == 1 else "Clear",
        accident=bool(row["accident"])
    ),
    axis=1
)

# Sonuclari CSV dosyasina kaydet
output_file = project_root / "data" / "processed" / "ml_dataset.csv"

df.to_csv(output_file, index=False)

print("\nML veri seti:", df.shape)

print("\nOrtalama bekleme suresi:")
print(df["average_wait_seconds"].mean())

print("\nMinimum bekleme suresi:")
print(df["average_wait_seconds"].min())

print("\nMaksimum bekleme suresi:")
print(df["average_wait_seconds"].max())

print("\nDosya kaydedildi:", output_file)


# ML hedef degiskeninin dogrulanmasi
assert len(df) == 720, "Beklenmeyen senaryo sayisi"

assert df["average_wait_seconds"].notna().all(), \
    "Eksik bekleme suresi bulundu"

assert (df["average_wait_seconds"] >= 0).all(), \
    "Negatif bekleme suresi bulundu"

assert (df["best_main_green"] + df["best_side_green"] == 54).all(), \
    "Gecersiz yesil isik suresi bulundu"

print("\nTum ML veri seti kontrolleri basarili.")