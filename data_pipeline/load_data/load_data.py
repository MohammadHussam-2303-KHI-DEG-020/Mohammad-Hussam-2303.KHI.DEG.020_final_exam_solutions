import os

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f"postgresql://postgres:{"456"}@db:5432/postgres")

data = pd.read_csv("/data/bookstore.csv")
data.to_sql("bookstore", engine)
