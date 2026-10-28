# Trafik Simülasyonu Kuralları

## Kavşak Yapısı
- Dört kollu, iki fazlı kavşak
- Ana yol: Kuzey-Güney
- Yan yol: Doğu-Batı
- Dönüş hareketleri ayrı modellenmeyecek

## Sinyalizasyon
- Toplam çevrim: 60 saniye
- Güvenlik geçişleri: toplam 6 saniye
- Dağıtılabilir yeşil süre: 54 saniye
- Minimum faz yeşili: 10 saniye
- Maksimum faz yeşili: 44 saniye

## Sinyalizasyon Planları
- Sabit zamanlı referans: 27/27 saniye
- Alternatif plan örneği: 36/18 saniye

## Geçiş Kapasitesi
- Normal koşullarda saniyede 0.5 araç
- Yağmurda geçiş kapasitesi %15 azalır
- Kazada etkilenen yolun kapasitesi %40 azalır

## Trafik Talebi
- Sabah ve akşam yoğun saatlerde araç gelişleri artar
- Etkinlikler ilgili yoldaki araç talebini artırır
- Hafta içi ve hafta sonu farklı trafik dağılımları kullanılır

## Kuyruk Mantığı
- Yeni gelen araçlar mevcut kuyruğa eklenir
- Yeşil ışıkta kapasite kadar araç geçebilir
- Geçemeyen araçlar sonraki çevrime aktarılır
- Kuyruk uzunluğu negatif olamaz

## Model Hedefi
- Ortalama araç bekleme süresini tahmin etmek
- Farklı yeşil ışık sürelerini karşılaştırmak
- Bekleme süresini azaltan uygun sinyalizasyon planını önermek

## Not
Bu değerler eğitim amaçlı sentetik simülasyon varsayımlarıdır.
Gerçek trafik ölçümlerine veya saha güvenlik standartlarına dayandıkları iddia edilmez.


## Veri Üretim Tasarımı

- Bir satır, bir trafik senaryosundaki 60 saniyelik çevrimi temsil eder.
- Her senaryoya benzersiz scenario_id atanır.
- Aynı senaryo farklı yeşil ışık süreleriyle test edilebilir.
- Yeşil süreler toplamı 54 saniye olmalıdır.
- Araç gelişleri ve başlangıç kuyrukları senaryoya aittir.
- Ortalama bekleme süresi kuyruk simülasyonundan hesaplanır.
- Bekleme süresi rastgele bir hedef değer olarak atanmaz.
- Eğitim ve test ayrımı scenario_id bazında yapılır.