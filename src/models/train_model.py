
from pathlib import Path

import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 1. Veri setini oku
project_root = Path(__file__).resolve().parents[2]

input_file = project_root / "data" / "processed" / "ml_dataset.csv"

df = pd.read_csv(input_file)


# 2. Model girdilerini belirle
feature_columns = [
    "hour",
    "day_of_week",
    "weather",
    "accident",
    "event_intensity",
    "main_road_vehicles",
    "side_road_vehicles",
    "best_main_green",
    "best_side_green"
]

X = df[feature_columns]
y = df["average_wait_seconds"]


# 3. Egitim ve test verilerini ayir
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Egitim verisi:", X_train.shape)
print("Test verisi:", X_test.shape)


# 4. Random Forest modelini olustur
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# 5. Modeli egit
model.fit(X_train, y_train)


# 6. Test verileriyle tahmin yap
predictions = model.predict(X_test)


# 7. Performans metriklerini hesapla
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANSI")
print("MAE:", round(mae, 3))
print("RMSE:", round(rmse, 3))
print("R2:", round(r2, 3))


# 8. Modeli kaydet
model_dir = project_root / "results" / "models"
model_dir.mkdir(parents=True, exist_ok=True)

model_path = model_dir / "random_forest_wait_time.joblib"

joblib.dump(model, model_path)

print("\nModel kaydedildi:", model_path)


# 9. Ornek tahminleri goster
comparison = pd.DataFrame({
    "actual_wait": y_test.to_numpy(),
    "predicted_wait": predictions
})

print("\nIlk 10 tahmin:")
print(comparison.head(10))


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