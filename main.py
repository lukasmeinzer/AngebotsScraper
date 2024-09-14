from utils import readToml, TableName
from Databasing.db_ops import is_new_week, table_into_db
from Bot.Logger import TelegramLogger

from Scraping.scraping import ProdukteCrawler
from Scraping.Aufbereitung import AufbereitungScraped

from Cleaning.Meta import CleanMeta
from Cleaning.Angebote import CleanAngebote


def main(TLog):
    url = readToml("URLs","Startpunkt")

    table_name = TableName()

    if is_new_week(table_name):
        TLog.neueMessage("neue Woche!")
    
        ProdukteCrawler(url, table_name)
        df_meta, df_angebote = AufbereitungScraped(table_name)  
    
        TLog.neueMessage("Crawling erfolgreich")
    
        df_meta = CleanMeta(df_meta = df_meta)
        df_angebote = CleanAngebote(df_angebote = df_angebote)
    
        TLog.neueMessage("Cleaning erfolgreich.")
    
    # Meta Informationen
        table_into_db(
        df=df_meta,
        db_name=readToml("DB_Names", "Meta"),
        table_name=table_name
    )
        table_into_db(
        df=df_meta, 
        db_name=readToml("DB_Names", "Meta"),
        table_name="latest_produkt"
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
        table_name="latest_markt"
    )
    
        TLog.neueMessage("Tabellen Insert erfolgreich.")
    
    else:
        TLog.neueMessage("Keine neue Woche.")


if __name__ == "__main__": 
    TLog = TelegramLogger("Initialisierung")
    
    try:
        main(TLog)
    except Exception as e:
        TLog.neueMessage(f"Exception occured: {str(e)}")
        
    TLog.release()
