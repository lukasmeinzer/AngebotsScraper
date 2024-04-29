import pandas as pd
import json

def AufbereitungScraped(table_name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    with open(f"{table_name}_scrapedData.json", "r") as infile: 
        data = json.load(infile)
    
    # cleanup the data a bit
    Angebote_columns = [
        "Produkt ID",
        "Produkt Name",
        "Angebot",
        "Filial ID",
        "Markt Name",
        "Gültig bis",
        "Preis",
        "Prozente",
        "kg/Li Preis",
    ]
    df_angebote = pd.DataFrame(columns=Angebote_columns)
        
    meta_rows_list = []
    for _, produkt_info in data.items():
        # für df_meta
        var_name = produkt_info["meta_data_1"]["name"]
        var_imageLink = produkt_info["meta_data_1"]["image"][0]
        try:
            var_preisEinheit = produkt_info["meta_data_1"]["offers"]["priceCurrency"]
            var_niedrigsterPreis = produkt_info["meta_data_1"]["offers"]["lowPrice"]
            var_anzahlAngebote = produkt_info["meta_data_1"]["offers"]["offerCount"]
            var_gültigBis = produkt_info["meta_data_1"]["offers"]["priceValidUntil"]
        except:
            var_preisEinheit = pd.NA
            var_niedrigsterPreis = pd.NA
            var_anzahlAngebote = pd.NA
        var_herstellerTyp = produkt_info["meta_data_1"]["manufacturer"]["@type"]
        var_herstellerName = produkt_info["meta_data_1"]["manufacturer"]["name"]
        var_ursprungsURL = produkt_info["meta_data_2"]["itemListElement"][-1]["item"]["@id"]
        var_kategorie = produkt_info["meta_data_2"]["itemListElement"][1]["item"]["name"]
        var_Gruppe = produkt_info["meta_data_2"]["itemListElement"][2]["item"]["name"]
        var_uvp =  produkt_info["uvp"]
        try:
            var_uvpKgLiPreis = produkt_info["kgPreis"]
        except:
            var_uvpKgLiPreis = pd.NA
        var_sorteInhalt = produkt_info["sorte_inhalt"]
        var_produktID = produkt_info["produkt_id"]
        
        meta_row = {
            "Name": var_name,
            "ImageLink": var_imageLink,
            "Preiseinheit": var_preisEinheit,
            "niedrigster Preis": var_niedrigsterPreis,
            "Anzahl Angebote": var_anzahlAngebote,
            "Gültig bis": var_gültigBis,
            "Hersteller Typ": var_herstellerTyp,
            "Hersteller Name": var_herstellerName,
            "Ursprungs URL": var_ursprungsURL,
            "Kategorie": var_kategorie,
            "Gruppe": var_Gruppe,
            "UVP": var_uvp,
            "UVP kg/Li Preis": var_uvpKgLiPreis,
            "Sorte/Inhalt": var_sorteInhalt,
            "Produkt ID": var_produktID,
        }
    
        meta_rows_list.append(meta_row)
    
    
        # für df_Angebote
        angebots_rows_list = []
        for markt, markt_info in produkt_info.items():
            if "Angebote" not in markt:
                continue
            var_angebot = markt_info["Angebot"]
            if var_angebot == "Nein":
                angebots_row = {
                    "Produkt ID": var_produktID,
                    "Produkt Name": var_name,
                    "Angebot": var_angebot,
                    "Filial ID": pd.NA,
                    "Markt Name": pd.NA,
                    "Gültig bis": pd.NA,
                    "Preis": pd.NA,
                    "Prozente": pd.NA,
                    "kg/Li Preis": pd.NA
                }
            else:
                var_filialID = markt_info["Filial ID"]
                var_marktName = markt.rsplit(" Angebote", maxsplit=1)[0]
                try:
                    var_angebotGültigBis = markt_info["gültig_bis"]
                except:
                    var_angebotGültigBis = pd.NA
                try:
                    var_preis = markt_info["preis"]
                except:
                    var_preis = pd.NA
                try:
                    var_prozente = markt_info["prozente"]
                except:
                    var_prozente = pd.NA
                try:
                    var_kgLiPreis = markt_info["neuer_kgPreis"] 
                except:
                    var_kgLiPreis = pd.NA
                angebots_row = {
                    "Produkt ID": var_produktID,
                    "Produkt Name": var_name,
                    "Angebot": var_angebot,
                    "Filial ID": var_filialID,
                    "Markt Name": var_marktName,
                    "Gültig bis": var_angebotGültigBis,
                    "Preis": var_preis,
                    "Prozente": var_prozente,
                    "kg/Li Preis": var_kgLiPreis
                }
            
            angebots_rows_list.append(angebots_row)
        
        df_angebote = pd.concat([df_angebote, pd.DataFrame(angebots_rows_list)]).reset_index(drop=True)
    
    df_meta = pd.DataFrame(meta_rows_list)
    
    df_meta["Datum Datenabzug"] = pd.to_datetime("today").normalize()
    df_angebote["Datum Datenabzug"] = pd.to_datetime("today").normalize()
    
    return df_meta, df_angebote
