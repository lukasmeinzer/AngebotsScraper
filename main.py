from utils import readToml, TableName
from Databasing.db_api import is_new_week, table_into_db
from Scraping.scraping import ProdukteCrawler
from Aufbereitung.Scraped import AufbereitungScraped

# Print-Statements werden gelogged

url = readToml("URLs","Startpunkt")

table_name = TableName()

if is_new_week(table_name):
    print("Neue Woche ...")
    
    ProdukteCrawler(url, table_name)
    df_meta, df_angebote = AufbereitungScraped(table_name)  
    
    # Meta Informationen
    table_into_db(
        df=df_meta,
        db_name=readToml("DB_Names", "Meta"),
        table_name=table_name, 
        type="raw"
    )
    table_into_db(
        df=df_meta, 
        db_name=readToml("DB_Names", "Meta"),
        table_name="latest", 
        type="raw"
    )

    # Angebots Informationen
    table_into_db(
        df=df_angebote, 
        db_name=readToml("DB_Names", "Angebote"),
        table_name=table_name, 
        type="raw"
    )
    table_into_db(
        df=df_angebote, 
        db_name=readToml("DB_Names", "Angebote"),
        table_name="latest", 
        type="raw"
    )
    
    print("... Crawling erfolgreich!")
else:
    print("Keine neue Woche")
