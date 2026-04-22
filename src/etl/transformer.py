# src/etl/transformer.py
import pandas as pd

class DataTransformer:
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        # Sütun isimlerini güvene alalım
        # yfinance columns might vary slightly, but we expect these
        cols_to_keep = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df[[c for c in cols_to_keep if c in df.columns]].copy()
        
        # Eksik verileri doldur/sil (BIST kapalı günleri vs.)
        df.dropna(subset=['Close'], inplace=True)
        
        # Hesaplamaları Ticker bazında yapmalıyız
        df.sort_values(by=['Ticker', 'Date'], inplace=True)
        
        # Günlük Getiri (Daily Return)
        df['Daily_Return'] = df.groupby('Ticker')['Close'].pct_change()
        
        # 50 Günlük Hareketli Ortalama (SMA_50)
        df['SMA_50'] = df.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=50, min_periods=1).mean())
        
        # 20 Günlük Volatilite (20d Volatility - Günlük getirilerin standart sapması)
        df['Volatility_20d'] = df.groupby('Ticker')['Daily_Return'].transform(lambda x: x.rolling(window=20, min_periods=1).std())
        
        # İlk günlerin pct_change ve std NaN olacaktır, onları 0 yapabiliriz
        df.fillna({'Daily_Return': 0, 'Volatility_20d': 0}, inplace=True)
        
        return df
