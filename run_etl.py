# run_etl.py
import os
import sys
from dotenv import load_dotenv
from src.etl.extractor import DataExtractor
from src.etl.transformer import DataTransformer
from src.etl.loader import DataLoader

def main():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("UYARI: DATABASE_URL environment variable is not set! Lütfen .env dosyasını kontrol edin.")
        sys.exit(1)

    tickers = ["THYAO.IS", "GARAN.IS", "TUPRS.IS", "YKBNK.IS", "FROTO.IS", "TOASO.IS", "AYGAZ.IS", "ARCLK.IS"]
    
    print(f"BIST 30 verileri çekiliyor: {tickers}")
    extractor = DataExtractor(tickers=tickers)
    raw_data = extractor.extract_data(period="2y")
    
    if raw_data.empty:
        print("KRİTİK HATA: Hiç veri çekilemedi. yfinance API'sinde bir sorun olabilir.")
        sys.exit(1)

    print("Veri dönüştürülüyor ve metrikler hesaplanıyor...")
    transformer = DataTransformer()
    clean_data = transformer.transform_data(raw_data)
    
    print(f"Veri veritabanına yükleniyor... ({len(clean_data)} satır)")
    loader = DataLoader(db_url)
    
    try:
        clean_data.to_sql(name="financial_data", con=loader.engine, if_exists="replace", index=False)
        print("Başarılı: 'financial_data' tablosu güncellendi.")
    except Exception as e:
        print(f"Hata: Veri yüklenirken bir problem oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
