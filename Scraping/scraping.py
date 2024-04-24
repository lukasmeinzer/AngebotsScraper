import sys
from colorama import Fore, Style
import requests
import json
from bs4 import BeautifulSoup


def ProdukteCrawler(url: str, table_name: str):
    AngebotsSeiten = get_all_urls(url)
    # dauert bissi:
    ProduktSeiten = get_all_products(AngebotsSeiten)
    
    all_offers = extract_data(ProduktSeiten) 
    
    with open(f"{table_name}_scrapedData.json", "w") as outfile: 
        json.dump(all_offers, outfile)
        

def get_all_products(AngebotsSeiten: list) -> list:
    ProduktSeiten = []
    
    for Seite in AngebotsSeiten:
        Seite = "https://www.aktionspreis.de" + Seite
        response = requests.get(Seite)

        if response.status_code != 200:
            print(f'{Fore.YELLOW}{Seite} could not be reached.{Style.RESET_ALL}')
            return 

        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        alle_urls = soup.find_all("a", attrs={"href": True})
        
        for url in alle_urls:
            href = url.get("href")
            if '/angebote/' in href:
                href = "/angebote/" + href.split("/")[-1] # Supermarkt Namen aus Link rausnehmen
                ProduktSeiten.append(href)
                
    return list(set(ProduktSeiten))


def get_all_urls(url: str) -> list:
    anbietende_Märkte=[]
    response = requests.get(url)

    if response.status_code != 200:
        print(f'{Fore.YELLOW}{url} could not be reached.{Style.RESET_ALL}')
        return 

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    alle_urls = soup.find_all("a", attrs={"href": True})
    
    for url in alle_urls:
        href = url.get("href")
        if '/prospekt/' in href:
            anbietende_Märkte.append(href)
        
    return list(set(anbietende_Märkte))



def extract_data(ProduktSeiten) -> dict:

    all_data = {}

    for i, url in enumerate(ProduktSeiten):
        # for Debugging:
        # sys.stdout.write(f"\rScraping offered products: ({i+1}/{len(ProduktSeiten)})")
        # sys.stdout.flush()

        url_text = url.rsplit("/", maxsplit=1)[1]
        url = "https://www.aktionspreis.de" + url
        response = requests.get(url)

        if response.status_code != 200:
            print(f'{Fore.YELLOW}{url} could not be reached.{Style.RESET_ALL}')
            all_data[url_text] = "nicht erreichbar"
            continue


        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        url_data = {}
        
        
        # Meta Data
        script_tag = soup.find_all('script', type='application/ld+json')
        meta_data_1 = script_tag[0]
        meta_data_2 = script_tag[1]
        
        url_data["meta_data_1"] = json.loads(meta_data_1.string)
        url_data["meta_data_2"] = json.loads(meta_data_2.string)
        
        
        try:
            url_data["uvp"] = soup.find('span', style='color:#5a5a5a;display:inline-block;padding-top:28px;font-weight:bold;font-size:13px;').text
        except:
            pass
        try:
            url_data["kgPreis"] = soup.find('span', style='float:right;display:inline-block;color:#fff;background:#7c7c7c;border-radius:5px; padding:0 5px 0 5px;').text
        except:
            pass
        try:
            url_data["name"] = soup.find(id='product_name').text
        except:
            pass
        try:
            url_data["sorte_inhalt"] = soup.find(id='sorte_inhalt').text
        except:
            pass
        try:
            url_data["produkt_id"] = soup.find('footer').find('span', style='color:#515151').text
        except:
            pass

        try:
            table_rows = soup.find_all('tr', attrs={'onmouseover': True})
        except:
            print(f'{Fore.YELLOW}{url} could not be scraped.{Style.RESET_ALL}')
            url_data["Angebot"] = "keine Tabelle gefunden"
            all_data[url_text]
            continue


        for row in table_rows:
            Angebots_data = {}
            
            row_contents = row.find_all("td")
            if len(row_contents) != 3:
                continue
            row_contents = row_contents[:-1] # last element in list is always irrelevant
            
            Supermarkt = row_contents[0].find("div").get("title")
            
            if row.find("span", style="display:inline-block; background:#cdcdcd; color:#fff; padding:2px 8px 1px 8px"):
                # Kein Angebot verfügbar
                Angebots_data["Angebot"] = "Nein"
                url_data[Supermarkt] = Angebots_data
                continue
            
            # Angebot verfügbar:
            Angebots_data["Angebot"] = "Ja"
            Angebots_data["Filial ID"] = row.attrs["onmouseover"]

            div_tag = row_contents[1].find("div")
            try:
                Angebots_data["gültig_bis"] = div_tag.find("span", style="font-size:8px").text
            except:
                pass
            try:
                Angebots_data["preis"] = div_tag.find("span", style="display:inline-block; background:#c03938; color:#fff; padding:2px 8px 1px 8px;font-size:12px;").text
            except:
                pass
            try:
                Angebots_data["prozente"] = div_tag.find("span", style="display:inline-block; background:#5a5a5a; color:#fff; padding:2px 8px 1px 8px; margin-left:2px;font-size:12px;").text
            except:
                pass
            try:
                Angebots_data["neuer_kgPreis"] = div_tag.find("small").text                    
            except:
                pass

            
            url_data[Supermarkt] = Angebots_data
    
        all_data[url_text] = url_data

    return all_data


