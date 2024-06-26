from sqlalchemy import create_engine, MetaData

import pandas as pd
from utils import DbConnectionString


def is_new_week(table_name: str) -> bool:
    
    # einfach irgendeine DB wählen.
    # Werden jedesmal zusammen abgezogen
    db_name = "MarktAngebote"
    engine = create_engine(DbConnectionString(db_name))
    
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    tables = list(metadata.tables.keys())
    engine.dispose()
    
    if any([table_name in table for table in tables]):
        return False
    return True
    
def table_into_db(
    df: pd.DataFrame, 
    db_name: str,
    table_name: str
    ):
    
    engine = create_engine(DbConnectionString(db_name))
    
    df.to_sql(f"{table_name}".lower(), engine, if_exists="replace", index=False)
    
    engine.dispose()
    
def table_from_db(
    db_name: str,
    table_name: str
    ) -> pd.DataFrame:
    
    engine = create_engine(DbConnectionString(db_name))
    connection =  engine.connect()
    
    df = pd.read_sql_table(f"{table_name}", connection)
    
    engine.dispose()
    
    return df
