# src/app/app.py
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Sayfa ayarları
st.set_page_config(page_title="BIST 30 Financial Dashboard", layout="wide")

# Ortam değişkenlerini yükle
load_dotenv()
db_url = os.getenv("DATABASE_URL")

@st.cache_data(ttl=600) # Önbelleği 10 dakikaya düşürelim (hızlı test için)
def load_data_from_db():
    if not db_url:
        st.error("DATABASE_URL bulunamadı. Lütfen Secrets ayarlarını kontrol edin.")
        return pd.DataFrame()
        
    try:
        # SQLAlchemy 2.0 uyumlu bağlantı
        engine = create_engine(db_url)
        
        # Sorun giderme: Mevcut tabloları listele
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            st.write(f"Veritabanındaki Tablolar: {tables}")
            
        query = text("SELECT * FROM financial_data ORDER BY \"Date\" ASC")
        
        with engine.connect() as conn:
            df = pd.read_sql(query, con=conn)
        return df
    except Exception as e:
        st.error(f"DETAYLI HATA: {e}")
        return pd.DataFrame()

def main():
    st.title("📈 BIST 30 Finansal Veri Paneli")
    st.markdown("Bu panel, PostgreSQL veritabanından çekilen güncel BIST 30 hisse verilerini gösterir.")
    
    with st.spinner('Veriler veritabanından getiriliyor...'):
        df = load_data_from_db()
    
    if df.empty:
        st.info("Henüz görüntülenecek veri yok. Eğer ETL yeni çalıştıysa lütfen 1-2 dakika bekleyip sayfayı yenileyin.")
        return
        
    # Hisse seçimi
    tickers = df['Ticker'].unique()
    selected_ticker = st.selectbox("Bir Hisse Senedi Seçin:", tickers)
    
    # Seçilen hisseye göre filtrele
    ticker_df = df[df['Ticker'] == selected_ticker].copy()
    
    # Tarih sütununu düzelt
    ticker_df['Date'] = pd.to_datetime(ticker_df['Date'])
    
    # Grafikler
    st.subheader(f"{selected_ticker} Fiyat ve SMA 50 Grafiği")
    
    chart_data = ticker_df.set_index('Date')[['Close', 'SMA_50']]
    st.line_chart(chart_data)
    
    # Metrikler
    st.subheader("Son Gün İstatistikleri")
    last_day = ticker_df.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kapanış", f"{last_day['Close']:.2f} TL")
    col2.metric("Günlük Getiri", f"% {last_day['Daily_Return']*100:.2f}")
    col3.metric("SMA (50 Gün)", f"{last_day['SMA_50']:.2f} TL")
    col4.metric("Volatilite (20 Gün)", f"{last_day['Volatility_20d']:.4f}")

if __name__ == "__main__":
    main()
