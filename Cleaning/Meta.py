import pandas as pd
import numpy as np

from Cleaning.AllgemeinCleaning import ersetzeUmlaute
from Cleaning.AllgemeinLogik import make_ID_unique


def CleanMeta(df_meta: pd.DataFrame):

    df = df_meta.copy()

    ### Cleaning
    
    df["niedrigster Preis"] = df["niedrigster Preis"].replace(pd.NA, np.nan).astype(float)
    df["Gültig bis"] = pd.to_datetime(df["Gültig bis"])
    
    lst_betroffene_Spalten = ["Name", "Hersteller Name", "Kategorie", "Gruppe", "Sorte/Inhalt"]
    df = ersetzeUmlaute(df, lst_betroffene_Spalten)
    
    df["Produkt ID"] = df["Produkt ID"].str.strip("Produkt-ID:").str.strip()
    
    df[["Sorte", "Inhalt"]] = df["Sorte/Inhalt"].str.split("-", n=1, expand=True)
    f_keinInhalt = df["Inhalt"].isna()
    df.loc[f_keinInhalt, "Inhalt"] = df["Sorte"].copy()
    df.loc[f_keinInhalt, "Sorte"] = pd.NA
    del df["Sorte/Inhalt"]
    
    df["UVP"] = (
        df["UVP"]    
        .str.strip("UVP:")
        .str.strip("€")
        .str.strip()
        .str.replace(",", ".")
        .replace("", np.nan)
        .astype(float)
    )
    
    if df["UVP kg/Li Preis"].notna().any():
        df[["UVP je Anteil", "Anteil"]] = df["UVP kg/Li Preis"].str.split(" je ", expand=True)
        df["UVP je Anteil"] = df["UVP je Anteil"].str.strip("€").str.strip().str.replace(",", ".")
    else:
        df[["UVP je Anteil", "Anteil"]] = pd.NA
    del df["UVP kg/Li Preis"]
    
    ### Logik
    
    df = make_ID_unique(df, namensspalte = "Name")
    
    assert (df.groupby("Produkt ID")["Name"].nunique() == 1).all(), "Es gibt mehrere Namen für eine Produkt ID."
    
    ### Ende
    
    return df