import pandas as pd

def make_ID_unique(df: pd.DataFrame, namensspalte: str) -> pd.DataFrame:
        
    df["tmp_Namenlänge"] = df[namensspalte].str.len()
    df = df.sort_values("tmp_Namenlänge", ascending=False)
    del df["tmp_Namenlänge"]
    
    eindeutige_Namen_je_ID = (
        df.groupby("Produkt ID")[namensspalte]
        .apply(lambda x: x.iloc[0])
        .drop_duplicates()
    ) 
    
    df = df.loc[df[namensspalte].isin(eindeutige_Namen_je_ID)]
    df = df.drop_duplicates([col for col in df.columns if col not in [namensspalte, "Ursprungs URL", "ImageLink"]], keep="first")
    return df

    