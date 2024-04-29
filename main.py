from utils import readToml, TableName
from Databasing.db_ops import is_new_week, table_into_db

from Scraping.scraping import ProdukteCrawler
from Scraping.Aufbereitung import AufbereitungScraped

from Cleaning.Meta import CleanMeta
from Cleaning.Angebote import CleanAngebote

# Print-Statements werden gelogged

url = readToml("URLs","Startpunkt")

table_name = TableName()

if is_new_week(table_name):
    print("Neue Woche ...")
    
    ProdukteCrawler(url, table_name)
    df_meta, df_angebote = AufbereitungScraped(table_name)  
    
    print("... Crawling erfolgreich")
    
    df_meta = CleanMeta(df_meta = df_meta)
    df_angebote = CleanAngebote(df_angebote = df_angebote)
    
    print("... Cleaning erfolgreich")
    
    # Meta Informationen
    table_into_db(
        df=df_meta,
        db_name=readToml("DB_Names", "Meta"),
        table_name=table_name
    )
    table_into_db(
        df=df_meta, 
        db_name=readToml("DB_Names", "Meta"),
        table_name="latest"
    )

    # Angebots Informationen
    table_into_db(
        df=df_angebote, 
        db_name=readToml("DB_Names", "Angebote"),
        table_name=table_name
    )
    table_into_db(
        df=df_angebote, 
        db_name=readToml("DB_Names", "Angebote"),
        table_name="latest"
    )
    
    print("... Tabellen Insert erfolgreich")
    
else:
    print("Keine neue Woche")
