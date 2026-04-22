import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import sys

# Sayfa ayarları
st.set_page_config(page_title="BIST 30 Financial Dashboard", layout="wide")

st.title("📈 BIST 30 Dashboard - Test Modu")
st.write(f"Python Sürümü: {sys.version}")

# Ortam değişkenlerini yükle
load_dotenv()
db_url = os.getenv("DATABASE_URL")

if not db_url:
    st.error("DATABASE_URL Secrets içinde bulunamadı!")
else:
    st.success("DATABASE_URL algılandı.")

def check_db():
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            # Sadece bağlantı testi
            conn.execute(text("SELECT 1"))
            st.success("Veritabanı bağlantısı başarılı!")
            
            # Tabloları listele
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            st.write(f"Mevcut Tablolar: {tables}")
            
            if "financial_data" in tables:
                df = pd.read_sql(text("SELECT * FROM financial_data LIMIT 5"), con=conn)
                st.write("Tablodan ilk 5 satır:")
                st.dataframe(df)
            else:
                st.warning("financial_data tablosu henüz oluşmamış!")
    except Exception as e:
        st.error(f"Bağlantı sırasında hata oluştu: {e}")

if st.button("Veritabanını Kontrol Et"):
    check_db()

st.write("Eğer bu yazıyı görüyorsanız, Streamlit başarıyla çalışıyor demektir.")
