# src/etl/loader.py
import pandas as pd
from sqlalchemy import create_engine

class DataLoader:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def load_data(self, df: pd.DataFrame, table_name: str = "financial_data"):
        if df.empty:
            print("No data to load.")
            return

        # PostgreSQL'e append ile yaz. 
        # Çift kaydı engellemek için pandas to_sql append yeterlidir ancak gerçek UPSERT
        # için daha kompleks bir sqlalchemy yapısı gerekir. Portfolio için if_exists='append' 
        # ve Date sütunu ile indeksleme iyi bir başlangıçtır.
        try:
            df.to_sql(name=table_name, con=self.engine, if_exists="append", index=False)
            print(f"Successfully loaded {len(df)} rows into {table_name}.")
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
