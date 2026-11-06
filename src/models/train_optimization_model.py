
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# 1. Dosya yollarini belirle
project_root = Path(__file__).resolve().parents[2]

input_file = (
    project_root
    / "data"
    / "processed"
    / "optimization_dataset.csv"
)

model_dir = project_root / "results" / "models"
model_dir.mkdir(parents=True, exist_ok=True)

model_path = model_dir / "random_forest_optimizer.joblib"


# 2. Veri setini oku
df = pd.read_csv(input_file)

feature_columns = [
    "hour",
    "day_of_week",
    "weather",
    "accident",
    "event_intensity",
    "main_road_vehicles",
    "side_road_vehicles",
    "main_green",
    "side_green"
]

X = df[feature_columns]
y = df["average_wait_seconds"]

groups = df["scenario_id"]


# 3. Senaryo bazli egitim/test ayrimi
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(X, y, groups=groups)
)

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

train_scenarios = set(groups.iloc[train_idx])
test_scenarios = set(groups.iloc[test_idx])

# Ayni senaryo hem egitim hem testte bulunmamali
assert train_scenarios.isdisjoint(test_scenarios)

print("Toplam veri:", len(df))
print("Egitim verisi:", X_train.shape)
print("Test verisi:", X_test.shape)

print("Egitim senaryosu:", len(train_scenarios))
print("Test senaryosu:", len(test_scenarios))


# 4. Random Forest modelini olustur
model = RandomForestRegressor(
    n_estimators=150,
    random_state=42,
    n_jobs=-1,
    min_samples_leaf=2
)


# 5. Modeli egit
print("\nModel egitiliyor...")

model.fit(X_train, y_train)

print("Model egitimi tamamlandi.")


# 6. Test verisiyle tahmin yap
predictions = model.predict(X_test)


# 7. Performans metriklerini hesapla
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANSI")
print("MAE:", round(mae, 3))
print("RMSE:", round(rmse, 3))
print("R2:", round(r2, 3))


# 8. Modeli ve gerekli bilgileri kaydet
model_bundle = {
    "model": model,
    "feature_columns": feature_columns,
    "train_scenarios": sorted(train_scenarios),
    "test_scenarios": sorted(test_scenarios)
}

joblib.dump(model_bundle, model_path)

print("\nModel kaydedildi:", model_path)


# 9. Ozellik onem siralamasi
importance = pd.DataFrame({
    "feature": feature_columns,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nOZELLIK ONEM SIRALAMASI")
print(importance.to_string(index=False))


# 10. Gercek hedef ve tahmin karsilastirmasi
comparison = pd.DataFrame({
    "actual_wait": y_test.to_numpy(),
    "predicted_wait": predictions
})

print("\nILK 10 TAHMIN")
print(comparison.head(10))


# 11. Son kontroller
assert len(df) == 25200
assert len(train_scenarios) == 576
assert len(test_scenarios) == 144
assert model_path.exists()

print("\nTum model kontrolleri basarili.")
