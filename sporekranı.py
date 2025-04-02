import requests
from bs4 import BeautifulSoup

def scrape_sporekrani():
    url = "https://www.sporekrani.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Bağlantı hatası:", response.status_code)
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Bugün olan verileri çekme
    today_section = soup.find("div", class_="col-12 date", string="Bugün")
    if today_section:
        today_events = today_section.find_all_next("div", class_="q-py-sm q-px-md event-item")
    else:
        today_events = []
    
    with open("veri.txt", "w", encoding="utf-8") as file:
        for event in today_events:
            # Logo URL belirleme
            logo_tag = event.select_one("img[data-src*='sports']")
            logo_url = logo_tag["data-src"] if logo_tag else "Bulunamadı"
            
            # Saat Bilgisi
            time_tag = event.select_one("span.text-body3-medium")
            match_time = time_tag.text.strip() if time_tag else "Bulunamadı"
            
            # Maç Adı
            match_name_tag = event.select_one("p.text-body3-bold")
            match_name = match_name_tag.text.strip() if match_name_tag else "Bulunamadı"
            
            # Kanal Bilgisi
            channel_tags = event.select("img[data-src*='channels']")
            channel_names = [channel_tag.get("title", "").strip() for channel_tag in channel_tags if channel_tag.get("title")]
            
            # Kanal adı 'TUTTUR TV' ise bir sonraki kanal bilgisini alalım
            for i in range(len(channel_names)):
                if channel_names[i].upper() == "TUTTUR TV" and i + 1 < len(channel_names):
                    main_channel = channel_names[i + 1]
                    break
            else:
                main_channel = channel_names[0] if channel_names else "Bulunamadı"
            
            # Özel kanal dönüşümleri
            channel_corrections = {
                "BEIN SPORTS 5": "BEIN SPORTS 5 HD",
                "HT SPOR": "HT SPOR HD",
                "TABII SPOR": "TABII SPOR HD",
                "TV100": "4K TR: TV100",
                "EUROSPORT": "EUROSPORT 1",
                "TV 8 BUÇUK": "TV 8.5"
            }
            main_channel = channel_corrections.get(main_channel.upper(), main_channel.upper())
            
            special_channels = {
                "BEIN SPORTS 1": ["BEIN SPORTS 8K FEED", "BEIN SPORTS 4K FEED", "BEIN SPORTS 1 H265"],
                "S SPORT PLUS": ["S-SPORT+1 MAC SAATI", "S-SPORT+2 MAC SAATI"]
            }
            
            if main_channel in special_channels:
                for spec_channel in special_channels[main_channel]:
                    output = f"MAÇ ADI= {match_name.upper()}\nSAAT= {match_time.upper()}\nKANAL= {spec_channel}\nLOGO URL= {logo_url}\n\n"
                    file.write(output)
            else:
                output = f"MAÇ ADI= {match_name.upper()}\nSAAT= {match_time.upper()}\nKANAL= {main_channel}\nLOGO URL= {logo_url}\n\n"
                file.write(output)

scrape_sporekrani()
