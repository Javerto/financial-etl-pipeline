# src/app/app.py
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Sayfa ayarları
st.set_page_config(page_title="BIST 30 Financial Dashboard", layout="wide")

# Ortam değişkenlerini yükle
load_dotenv()
db_url = os.getenv("DATABASE_URL")

@st.cache_data(ttl=3600) # Veriyi 1 saat boyunca cache'le
def load_data_from_db():
    if not db_url:
        st.error("DATABASE_URL bulunamadı. Lütfen .env dosyasını veya Secrets'i ayarlayın.")
        return pd.DataFrame()
        
    engine = create_engine(db_url)
    # PostgreSQL'de sütun isimleri ve tablo isimleri küçük harfe duyarlı olabilir, 
    # çift tırnak gerekebilir.
    query = "SELECT * FROM financial_data ORDER BY \"Date\" ASC"
    try:
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        st.error(f"Veritabanı bağlantı hatası: {e}")
        return pd.DataFrame()

def main():
    st.title("📈 BIST 30 Finansal Veri Paneli")
    st.markdown("Bu panel, PostgreSQL veritabanından çekilen güncel BIST 30 hisse verilerini gösterir.")
    
    df = load_data_from_db()
    
    if df.empty:
        st.warning("Veritabanında görüntülenecek veri bulunamadı. Lütfen önce run_etl.py betiğini çalıştırın.")
        return
        
    # Hisse seçimi
    tickers = df['Ticker'].unique()
    selected_ticker = st.selectbox("Bir Hisse Senedi Seçin:", tickers)
    
    # Seçilen hisseye göre filtrele
    ticker_df = df[df['Ticker'] == selected_ticker].copy()
    
    # Grafikler
    st.subheader(f"{selected_ticker} Fiyat ve SMA 50 Grafiği")
    
    # Streamlit line_chart için veriyi hazırlama
    ticker_df['Date'] = pd.to_datetime(ticker_df['Date'])
    chart_data = ticker_df.set_index('Date')[['Close', 'SMA_50']]
    st.line_chart(chart_data)
    
    # Metrikler (Son gün verisi)
    st.subheader("Son Gün İstatistikleri")
    last_day = ticker_df.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kapanış", f"{last_day['Close']:.2f} TL")
    col2.metric("Günlük Getiri", f"% {last_day['Daily_Return']*100:.2f}")
    col3.metric("SMA (50 Gün)", f"{last_day['SMA_50']:.2f} TL")
    col4.metric("Volatilite (20 Gün)", f"{last_day['Volatility_20d']:.4f}")

if __name__ == "__main__":
    main()
