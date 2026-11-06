
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "processed" / "ml_optimization_results.csv"
OUTPUT = ROOT / "docs" / "ai_traffic_analysis_report.md"

df = pd.read_csv(INPUT)

required = ["fixed_wait", "adaptive_wait", "ml_wait", "optimal_wait"]
missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Eksik sutunlar: {missing}")

if df.empty or df[required].isna().any().any():
    raise ValueError("Sonuc verisi bos veya eksik deger iceriyor.")

if (df[required] < 0).any().any():
    raise ValueError("Bekleme sureleri negatif olamaz.")

means = df[required].mean()

fixed = means["fixed_wait"]
adaptive = means["adaptive_wait"]
ml = means["ml_wait"]
optimal = means["optimal_wait"]

improvement = (fixed - ml) / fixed * 100 if fixed > 0 else 0
gap = ml - optimal

report = f"""# Yapay Zeka Destekli Trafik Optimizasyonu - Analiz Raporu

## 1. Projenin Amaci

Bu proje, trafik yogunluguna gore trafik isigi surelerinin
optimize edilmesini ve farkli sinyalizasyon yaklasimlarinin
bekleme suresi acisindan karsilastirilmasini amaclamaktadir.

## 2. Yontem

Projede sentetik trafik senaryolari olusturulmus ve
basitlestirilmis bir trafik simulasyonu kullanilmistir.

Random Forest Regression modeli, farkli trafik kosullari
ve yesil isik suresi dagilimlari icin bekleme suresini
tahmin etmek amaciyla egitilmistir.

## 3. Performans Sonuclari

Degerlendirilen test senaryosu sayisi: {len(df)}

| Yontem | Ortalama Bekleme Suresi |
|---|---:|
| Sabit sinyalizasyon | {fixed:.3f} sn |
| Adaptif sinyalizasyon | {adaptive:.3f} sn |
| ML tabanli sinyalizasyon | {ml:.3f} sn |
| Simulasyon optimumu | {optimal:.3f} sn |

ML tabanli yaklasim, sabit sinyalizasyona gore
%{improvement:.2f} oraninda daha dusuk ortalama
bekleme suresi elde etmistir.

ML yaklasiminin simulasyon optimumundan farki
{gap:.3f} saniyedir.

## 4. Sonuclarin Degerlendirilmesi

Sonuclar, olusturulan simulasyon kosullarinda
ML tabanli sinyalizasyonun sabit sinyalizasyondan
daha dusuk ortalama bekleme suresi sagladigini
gostermektedir.

Bu bulgular gercek trafik ortaminda ayni performansin
elde edilecegini garanti etmez.

## 5. Mistral AI Entegrasyonu

Projenin raporlama asamasinda, trafik optimizasyonu
sonuclarinin buyuk dil modeli yardimiyla dogal dilde
yorumlanmasi icin Mistral AI entegrasyonu denenmistir.

Python uzerinden Mistral API'ye HTTP istegi gonderilmis,
ancak API tarafindan HTTP 429 (Rate limit exceeded)
yaniti alinmistir.

Bu nedenle Mistral modelinden tamamlanmis bir analiz
yaniti elde edilememistir. Bu rapordaki sayisal analizler
Python ve Pandas kullanilarak hesaplanmistir.

Mistral AI, gelecekte API erisimi saglandiginda
sonuclarin otomatik yorumlanmasi ve raporlanmasi icin
kullanilabilecek yardimci bir bilesen olarak
degerlendirilmistir.

## 6. Sinirliliklar

- Veriler sentetik olarak olusturulmustur.
- Trafik simulasyonu gercek dunyayi tam olarak temsil etmez.
- Modelin gercek trafik verileriyle test edilmesi gereklidir.
- Mistral AI entegrasyonu API limitine takildigi icin tamamlanamamistir.

## 7. Genel Sonuc

Proje kapsaminda Random Forest Regression ile
trafik isigi suresi optimizasyonu gerceklestirilmis
ve farkli sinyalizasyon yontemleri karsilastirilmistir.

Elde edilen sonuclar, kullanilan simulasyon
kosullarinda ML tabanli yaklasimin potansiyelini
gostermektedir.
"""

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(report, encoding="utf-8")

print(f"Rapor olusturuldu: {OUTPUT}")
print(f"Test senaryosu: {len(df)}")
print(f"ML iyilesme: %{improvement:.2f}")
