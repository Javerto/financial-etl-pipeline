# tests/test_transformer.py
import pytest
import pandas as pd
import numpy as np
from src.etl.transformer import DataTransformer

def test_transform_data_adds_metrics():
    # Sahte veri oluştur
    dates = pd.date_range("2023-01-01", periods=100)
    data = {
        "Date": dates,
        "Ticker": ["THYAO.IS"] * 100,
        "Open": np.random.rand(100) * 100,
        "High": np.random.rand(100) * 100,
        "Low": np.random.rand(100) * 100,
        "Close": np.random.rand(100) * 100,
        "Volume": np.random.randint(1000, 10000, size=100)
    }
    df = pd.DataFrame(data)
    
    transformer = DataTransformer()
    transformed_df = transformer.transform_data(df)
    
    assert "Daily_Return" in transformed_df.columns
    assert "SMA_50" in transformed_df.columns
    assert "Volatility_20d" in transformed_df.columns
    # Sadece gerekli sütunların kaldığından emin ol
    assert set(["Date", "Ticker", "Open", "High", "Low", "Close", "Volume", "Daily_Return", "SMA_50", "Volatility_20d"]).issubset(transformed_df.columns)
