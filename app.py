import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Sayfa ayarları
st.set_page_config(page_title="BIST 30 Finansal Dashboard", layout="wide")

# Ortam değişkenlerini yükle
load_dotenv()
db_url = os.getenv("DATABASE_URL")

@st.cache_data(ttl=600) # Veriyi 10 dakika cache'le
def load_data_from_db():
    if not db_url:
        st.error("DATABASE_URL bulunamadı. Lütfen Secrets ayarlarını kontrol edin.")
        return pd.DataFrame()
        
    try:
        # SQLAlchemy 2.0 uyumlu bağlantı
        engine = create_engine(db_url)
        query = text("SELECT * FROM financial_data ORDER BY \"Date\" ASC")
        
        with engine.connect() as conn:
            df = pd.read_sql(query, con=conn)
        return df
    except Exception as e:
        st.error(f"Veritabanı bağlantı hatası: {e}")
        return pd.DataFrame()

def main():
    st.title("📈 BIST 30 Finansal Veri Paneli")
    st.markdown("Bu panel, PostgreSQL veritabanından çekilen güncel BIST 30 hisse verilerini gösterir.")
    
    with st.spinner('Veriler yükleniyor...'):
        df = load_data_from_db()
    
    if df.empty:
        st.info("Veritabanında henüz veri bulunamadı. Lütfen ETL boru hattının çalıştığından emin olun.")
        return
        
    # Hisse seçimi
    tickers = df['Ticker'].unique()
    selected_ticker = st.sidebar.selectbox("Bir Hisse Senedi Seçin:", tickers)
    
    # Seçilen hisseye göre filtrele
    ticker_df = df[df['Ticker'] == selected_ticker].copy()
    
    # Tarih formatını düzelt
    ticker_df['Date'] = pd.to_datetime(ticker_df['Date'])
    
    # Metrikler (En Üstte)
    last_day = ticker_df.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kapanış Fiyatı", f"{last_day['Close']:.2f} TL")
    col2.metric("Günlük Getiri", f"% {last_day['Daily_Return']*100:.2f}")
    col3.metric("SMA (50 Gün)", f"{last_day['SMA_50']:.2f} TL")
    col4.metric("20G Volatilite", f"{last_day['Volatility_20d']:.4f}")

    # Ana Grafik
    st.subheader(f"{selected_ticker} Fiyat ve Hareketli Ortalama (2 Yıllık)")
    chart_data = ticker_df.set_index('Date')[['Close', 'SMA_50']]
    st.line_chart(chart_data)
    
    # Detaylı Veri Tablosu (Opsiyonel)
    if st.checkbox("Ham Verileri Göster"):
        st.write(ticker_df.tail(20))

if __name__ == "__main__":
    main()
