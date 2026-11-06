# Yapay Zeka Destekli Trafik Optimizasyonu - Analiz Raporu

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

Degerlendirilen test senaryosu sayisi: 144

| Yontem | Ortalama Bekleme Suresi |
|---|---:|
| Sabit sinyalizasyon | 16.746 sn |
| Adaptif sinyalizasyon | 16.073 sn |
| ML tabanli sinyalizasyon | 15.933 sn |
| Simulasyon optimumu | 15.844 sn |

ML tabanli yaklasim, sabit sinyalizasyona gore
%4.86 oraninda daha dusuk ortalama
bekleme suresi elde etmistir.

ML yaklasiminin simulasyon optimumundan farki
0.089 saniyedir.

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
