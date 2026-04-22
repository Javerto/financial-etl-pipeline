# tests/test_extractor.py
import pytest
import pandas as pd
from src.etl.extractor import DataExtractor

def test_extract_data_returns_dataframe():
    extractor = DataExtractor(tickers=["THYAO.IS"])
    # 5 günlük küçük bir veri çekip test ediyoruz
    df = extractor.extract_data(period="5d")
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Open" in df.columns
    assert "Close" in df.columns
    assert "Ticker" in df.columns
