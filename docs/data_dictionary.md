# Trafik Veri Sozlugu

## Proje Kapsami

Tek bir dort kollu, iki fazli kavsagin trafik verileri.

## Veri Seti Yapisi

Bir satir, belirli bir trafik senaryosunda
60 saniyelik bir sinyal cevriminin sonucunu temsil eder.

## Kolonlar

| Kolon | Tip | Aciklama |
|---|---|---|
| scenario_id | int | Trafik senaryosu kimligi |
| hour | int | Saat (0-23) |
| day_of_week | int | Haftanin gunu (0-6) |
| weather | str | Hava durumu |
| accident | bool | Kaza var mi? |
| event_intensity | float | Etkinlik yogunlugu (0-1) |
| main_road_vehicles | int | Ana yola gelen arac sayisi |
| side_road_vehicles | int | Yan yola gelen arac sayisi |
| main_queue_start | int | Ana yol baslangic kuyrugu |
| side_queue_start | int | Yan yol baslangic kuyrugu |
| main_green_seconds | int | Ana yol yesil suresi |
| side_green_seconds | int | Yan yol yesil suresi |
| average_wait_seconds | float | Ortalama bekleme suresi |

## Makine Ogrenmesi

### Features
Arac sayilari, kuyruklar, trafik kosullari
ve yesil isik sureleri.

### Target
average_wait_seconds

Model, ortalama arac bekleme suresini
saniye cinsinden tahmin edecektir.
