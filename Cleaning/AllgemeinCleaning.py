import pandas as pd

def ersetzeUmlaute(df: pd.DataFrame, lst_betroffene_Spalten: list) -> pd.DataFrame:
    replace_dict = {
        "Ã¶": "ö",
        "Ã¼": "ü",
        "Ã¤": "ä",
        "ÃŸ": "ß",
        "Ã\x9f": "ß",
        "Ã„": "Ä",
        "Ã–": "Ö",
        "Ã\x96": "Ö",
        "Ãœ": "Ü",
        "Ã\x9c": "Ü",
        "Ã©": "é",
        "Ã¨": "è",
    }
    df[lst_betroffene_Spalten] = df[lst_betroffene_Spalten].replace(replace_dict, regex=True)
    
    return df
    