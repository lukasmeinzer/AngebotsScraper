import pandas as pd
import numpy as np

from Cleaning.AllgemeinCleaning import ersetzeUmlaute
from Cleaning.AllgemeinLogik import make_ID_unique

def CleanAngebote(df_angebote: pd.DataFrame):
    
    df = df_angebote.copy()
    
    ### Cleaning
    
    df["Produkt ID"] = df["Produkt ID"].str.strip("Produkt-ID:").str.strip()
    
    lst_betroffene_Spalten = ["Produkt Name", "Markt Name", "kg/Li Preis"]
    df = ersetzeUmlaute(df, lst_betroffene_Spalten)
    df = df.replace(r'^\s*$', np.nan, regex=True) # empty strings
    
    df["Filial ID"] = df["Filial ID"].str.extract(pat=r"'#filiale_(\d+)'")
    
    df["Gültig bis"] = pd.to_datetime(df["Gültig bis"].str.strip("bis "), format="%d.%m.%y")
    
    
    f_Ausnahme = df["Preis"].str.contains(r"Rabatt|Paypack|Punkte|%", case=False, na=False)
    df["Hinweis"] = pd.NA
    df.loc[f_Ausnahme, "Hinweis"] = df["Preis"].copy()
    df.loc[f_Ausnahme, "Preis"] = np.nan
    
    df["Preis"] = df["Preis"].str.strip(" €").str.replace(",", ".").replace(pd.NA, np.nan).astype(float)
    
    df["Prozente"] = df["Prozente"].str.strip("-").str.strip(" %").replace(pd.NA, np.nan).astype(float)
    
    df[["Preis je Anteil", "Anteil"]] = df["kg/Li Preis"].str.split(" je ", n=1, expand=True)
    
    f_Ausnahme = df["Preis je Anteil"].str.contains(r"beim Kauf|ClubCard|Kiste|Kasten|Karton|Versand", case=False, na=False)
    df["Preis je Anteil"] = df["Preis je Anteil"].str.strip("€").str.strip().str.replace(",", ".")
    df.loc[f_Ausnahme, "Hinweis"] = df["Preis je Anteil"].copy()
    df.loc[f_Ausnahme, "Preis je Anteil"] = pd.NA
    
    df[["Anteil", "Hinweis"]] = df["Anteil"].str.split("|", n=1, expand=True)
    df["Anteil"] = df["Anteil"].str.strip()
    df["Hinweis"] = df["Hinweis"].str.strip()
    
    del df["kg/Li Preis"]
    
    df["Preiseinheit"] = "EUR"
    
    ### Logik
    
    df = make_ID_unique(df, namensspalte = "Produkt Name")
    
    assert (df.groupby("Produkt ID")["Produkt Name"].nunique() == 1).all(), "Es gibt mehrere Namen für eine Produkt ID."
    
    df = df.loc[df["Angebot"] != "Nein"].copy()
    
    ### Ende
    
    return df
