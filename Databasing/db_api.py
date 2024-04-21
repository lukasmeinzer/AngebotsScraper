from sqlalchemy import create_engine, MetaData

import pandas as pd
from typing import Literal
from utils import DbConnectionString


def check_for_new_week(table_name: str):
    
    # einfach irgendeine DB wählen.
    # Werden jedesmal zusammen abgezogen
    db_name = "MarktAngebote"
    engine = create_engine(DbConnectionString(db_name))
    
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    tables = list(metadata.tables.keys())
    engine.dispose()
    
    if table_name in tables:
        return False
    return True
    
def insert_into_db(
    df: pd.DataFrame, 
    db_name: str,
    table_name: str, 
    type: Literal["raw","cleaned"],
    ):
    
    engine = create_engine(DbConnectionString(db_name))
    
    df.to_sql(f"{table_name}_{type}".lower(), engine, if_exists="replace", index=False)
    
    engine.dispose()