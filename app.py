import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Sayfa ayarları
st.set_page_config(page_title="BIST 30 Finansal Veri Paneli", layout="wide", page_icon="📈")

# Ortam değişkenlerini yükle
load_dotenv()
db_url = os.getenv("DATABASE_URL")

@st.cache_data(ttl=600) # Veriyi 10 dakika boyunca cache'le
def load_data_from_db():
    if not db_url:
        st.error("DATABASE_URL bulunamadı. Lütfen Secrets ayarlarını kontrol edin.")
        return pd.DataFrame()
        
    try:
        engine = create_engine(db_url)
        # PostgreSQL'de büyük/küçük harf duyarlılığı için "Date" çift tırnak içinde olmalı
        query = text("SELECT * FROM financial_data ORDER BY \"Date\" ASC")
        
        with engine.connect() as conn:
            df = pd.read_sql(query, con=conn)
        return df
    except Exception as e:
        st.error(f"Veritabanı hatası: {e}")
        return pd.DataFrame()

def main():
    st.title("📈 BIST 30 Finansal Veri Paneli")
    st.markdown("""
    Bu panel, **PostgreSQL** veritabanından çekilen güncel BIST 30 hisse verilerini gösterir. 
    Veriler her akşam 19:30'da **GitHub Actions** tarafından otomatik olarak güncellenir.
    """)
    
    with st.spinner('Veriler getiriliyor...'):
        df = load_data_from_db()
    
    if df.empty:
        st.info("Henüz görüntülenecek veri yok. Eğer ETL yeni çalıştıysa lütfen 1-2 dakika bekleyip sayfayı yenileyin.")
        return
        
    # Hisse seçimi
    tickers = sorted(df['Ticker'].unique())
    selected_ticker = st.selectbox("Bir Hisse Senedi Seçin:", tickers)
    
    # Seçilen hisseye göre filtrele
    ticker_df = df[df['Ticker'] == selected_ticker].copy()
    ticker_df['Date'] = pd.to_datetime(ticker_df['Date'])
    
    # Metrikler (Üst Panel)
    last_day = ticker_df.iloc[-1]
    prev_day = ticker_df.iloc[-2] if len(ticker_df) > 1 else last_day
    
    col1, col2, col3, col4 = st.columns(4)
    
    price_diff = last_day['Close'] - prev_day['Close']
    col1.metric("Son Kapanış", f"{last_day['Close']:.2f} TL", f"{price_diff:.2f} TL")
    
    return_val = last_day['Daily_Return'] * 100
    col2.metric("Günlük Getiri", f"% {return_val:.2f}")
    
    col3.metric("SMA (50 Gün)", f"{last_day['SMA_50']:.2f} TL")
    col4.metric("Volatilite (20 Gün)", f"{last_day['Volatility_20d']:.4f}")

    # Grafik Bölümü
    st.subheader(f"📊 {selected_ticker} Fiyat Analizi")
    
    # Grafik verisi hazırlama
    chart_data = ticker_df.set_index('Date')[['Close', 'SMA_50']]
    st.line_chart(chart_data)
    
    # Veri Tablosu (Opsiyonel)
    with st.expander("Ham Verileri Görüntüle"):
        st.dataframe(ticker_df.sort_values('Date', ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
