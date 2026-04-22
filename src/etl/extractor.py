# src/etl/extractor.py
import yfinance as yf
import pandas as pd
from typing import List

class DataExtractor:
    def __init__(self, tickers: List[str]):
        self.tickers = tickers

    def extract_data(self, period: str = "2y") -> pd.DataFrame:
        all_data = []
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            if not df.empty:
                df = df.reset_index()
                df["Ticker"] = ticker
                # yfinance timezone bilgisi getirebilir, onu kaldıralım
                df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
                all_data.append(df)
                
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()
