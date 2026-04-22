# 📈 BIST 30 Finansal ETL Boru Hattı & Dashboard

Bu proje, BIST 30 endeksindeki seçili hisselerin (THYAO, GARAN, TUPRS, YKBNK, FROTO, TOASO, AYGAZ, ARCLK) finansal verilerini otomatik olarak çeken, işleyen, bir PostgreSQL veritabanında saklayan ve interaktif bir Streamlit dashboard'u üzerinden sunan uçtan uca bir veri mühendisliği çözümüdür.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20(Neon)-green.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![GitHub Actions](https://img.shields.io/badge/Automation-GitHub%20Actions-black.svg)

## 🚀 Canlı Demo
- **Dashboard:** [BIST 30 Finansal Analiz Paneli](https://financial-etl-pipeline-lybpeg9k44r57fzxweigec.streamlit.app/)
- **Portfolyo Entegrasyonu:** [javerto.github.io](https://javerto.github.io)

## 🛠️ Mimari ve Teknolojiler

Proje, modüler bir **OOP (Nesne Yönelimli Programlama)** yapısı üzerine kurulmuştur:

1.  **Veri Çekme (Extractor):** `yfinance` API kullanılarak BIST 30 hisselerinin son 2 yıllık geçmiş verileri çekilir.
2.  **Veri Dönüştürme (Transformer):** Pandas kullanılarak veriler temizlenir ve finansal metrikler hesaplanır:
    -   **SMA_50:** 50 Günlük Hareketli Ortalama.
    -   **Daily Return:** Günlük yüzde getiri.
    -   **Volatility:** 20 günlük hareketli volatilite.
3.  **Veri Yükleme (Loader):** SQLAlchemy 2.0 kullanılarak işlenmiş veriler **Neon PostgreSQL** veritabanına `replace` stratejisi ile aktarılır.
4.  **Otomasyon:** GitHub Actions üzerinde kurulan **Cron Job** ile her hafta içi saat **19:30 TSİ (16:30 UTC)**'da boru hattı otomatik olarak tetiklenir.
5.  **Görselleştirme:** Streamlit Cloud üzerinde barındırılan dashboard, veritabanına doğrudan bağlanarak güncel analizleri sunar.

## 📁 Proje Yapısı

```text
├── .github/workflows/   # GitHub Actions otomasyon tanımları
├── src/
│   ├── etl/             # ETL sınıfları (Extractor, Transformer, Loader)
│   └── app/             # Dashboard kaynak kodları (Arşiv)
├── app.py               # Ana Streamlit Dashboard dosyası
├── run_etl.py           # ETL orkestrasyon betiği
└── requirements.txt     # Bağımlılıklar
```

## 🔧 Kurulum ve Çalıştırma

Yerelde çalıştırmak isterseniz:

1.  Repoyu klonlayın: `git clone https://github.com/Javerto/financial-etl-pipeline.git`
2.  Bağımlılıkları yükleyin: `pip install -r requirements.txt`
3.  `.env` dosyası oluşturun ve veritabanı bağlantı bilginizi ekleyin:
    ```env
    DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
    ```
4.  ETL'i çalıştırın: `python run_etl.py`
5.  Dashboard'u başlatın: `streamlit run app.py`

## 📊 Öne Çıkan Özellikler
-   **Bulut Tabanlı:** Tamamen sunucusuz (serverless) mimari (GitHub Actions + Neon DB + Streamlit Cloud).
-   **Hata Yönetimi:** Veri çekme veya yükleme sırasında oluşabilecek hatalar için loglama ve GitHub Actions üzerinden bildirim mekanizması.
-   **Entegrasyon:** Başka web sitelerine (GitHub Pages gibi) kolayca embed edilebilir yapı.

---
**Geliştiren:** [Yiğit Tenekeci](https://javerto.github.io)
