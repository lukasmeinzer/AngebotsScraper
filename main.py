from utils import readToml, TableName
from Databasing.db_api import check_for_new_week, insert_into_db
from Scraping.scraping import ProdukteCrawler
from Cleaning.CleanScraped import ScrapingAufbereitung

# Print-Statements werden gelogged

url = readToml("URLs","Startpunkt")

table_name = TableName()
is_new_week = check_for_new_week(table_name)

if is_new_week:
    print("Neue Woche ...")
    ProdukteCrawler(url, table_name)
    df_meta, df_angebote = ScrapingAufbereitung(table_name)  
    
    # Meta Informationen
    insert_into_db(
        df=df_meta,
        db_name="MarktMeta",
        table_name=table_name, 
        type="raw"
    )
    insert_into_db(
        df=df_meta, 
        db_name="MarktMeta",
        table_name="latest", 
        type="raw"
    )

    # Angebots Informationen
    insert_into_db(
        df=df_angebote, 
        db_name="MarktAngebote",
        table_name=table_name, 
        type="raw"
    )
    insert_into_db(
        df=df_angebote, 
        db_name="MarktAngebote",
        table_name="latest", 
        type="raw"
    )
    print("... Crawling erfolgreich!")

else:
    print("Keine neue Woche")
