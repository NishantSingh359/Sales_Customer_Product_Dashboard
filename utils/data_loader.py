import pandas as pd
from sqlalchemy import create_engine

user = "root"
password = "1234"
host = "localhost"
database = "gold"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

def load_gold() -> None:
    """
    Load data from SQL Database
    """
    tables = ['dim_customer', 'dim_product', 'fact_sales']

    for tbl_name in tables:
        df = pd.read_sql(f"SELECT * FROM {tbl_name}", con=engine)
        df.to_csv(f"data/{tbl_name}.csv", index=False)
   
def create_date_table() -> None:

    sales = pd.read_csv(r"data/fact_sales.csv", parse_dates=['order_date'])
    start_date:str = sales['order_date'].min()
    end_date:str = sales['order_date'].max()

    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    df = pd.DataFrame({'full_date': dates})

    df['date_key'] = df['full_date'].dt.strftime('%Y%m%d').astype(int) #type: ignore
    df['year'] = df['full_date'].dt.year #type: ignore
    df['quarter'] = df['full_date'].dt.quarter #type: ignore
    df['month'] = df['full_date'].dt.month #type: ignore
    df['month_name'] = df['full_date'].dt.month_name() #type: ignore
    df['week'] = df['full_date'].dt.isocalendar().week #type: ignore
    df['day'] = df['full_date'].dt.day #type: ignore
    df['day_name'] = df['full_date'].dt.day_name() #type: ignore
    df['is_weekend'] = df['day_name'].isin(['Saturday', 'Sunday'])

    df = df.to_csv(r"data\dim_date.csv", index=False)

def main():
    load_gold()
    create_date_table()

if __name__ == "__main__":
    main()

