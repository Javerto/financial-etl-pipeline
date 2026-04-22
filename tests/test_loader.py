# tests/test_loader.py
import pytest
import pandas as pd
from sqlalchemy import create_engine
from src.etl.loader import DataLoader

def test_load_data_to_sqlite():
    # Test için in-memory SQLite kullanıyoruz
    db_url = "sqlite:///:memory:"
    df = pd.DataFrame({
        "Date": [pd.Timestamp("2023-01-01")],
        "Ticker": ["THYAO.IS"],
        "Close": [100.5]
    })
    
    loader = DataLoader(db_url)
    loader.load_data(df, table_name="financial_data")
    
    # Aynı engine üzerinden okuma yapmalıyız
    result_df = pd.read_sql("SELECT * FROM financial_data", con=loader.engine)
    
    assert len(result_df) == 1
    assert result_df.iloc[0]["Ticker"] == "THYAO.IS"
