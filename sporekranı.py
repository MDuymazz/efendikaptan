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
            logo_alt = logo_tag["alt"] if logo_tag else ""
            
            logo_map = {
                "Programlar": "https://t4.ftcdn.net/jpg/01/57/34/25/360_F_157342588_54ZpX48MoK3mdBh0PqnwWdQnMY3KDB29.jpg",
                "Basketbol": "https://w7.pngwing.com/pngs/37/428/png-transparent-basketball-tennis-balls-ball-sport-orange-sphere-thumbnail.png",
                "Tenis": "https://w7.pngwing.com/pngs/392/642/png-transparent-tennis-balls-logo-ball-logo-pickup-sphere.png",
                "Binicilik": "https://w7.pngwing.com/pngs/497/39/png-transparent-horse-equestrian-mule-track-stallion-horse-horse-child-animals.png",
                "Futbol": "https://st4.depositphotos.com/11498520/21397/v/950/depositphotos_213977444-stock-illustration-soccer-ball-vector-football-logo.jpg",
                "Voleybol": "https://w7.pngwing.com/pngs/743/385/png-transparent-volleyball-volleyball-sport-logo-volleyball-thumbnail.png",
                "Alp Disiplini": "https://e7.pngegg.com/pngimages/759/940/png-clipart-cross-country-skiing-snowboarding-alpine-skiing-skiing-angle-sport-thumbnail.png",
                "Bisiklet": "https://st3.depositphotos.com/1768926/19164/v/950/depositphotos_191646480-stock-illustration-bike-logo-icon-design-template.jpg"
            }
            
            logo_url = logo_map.get(logo_alt, "Bulunamadı")
            
            # Saat Bilgisi
            time_tag = event.select_one("span.text-body3-medium")
            match_time = time_tag.text.strip() if time_tag else "Bulunamadı"
            
            # Maç Adı
            match_name_tag = event.select_one("p.text-body3-bold")
            match_name = match_name_tag.text.strip() if match_name_tag else "Bulunamadı"
            
            # Kanal Bilgisi: S Sport veya diğer kanallar
            channel_tags = event.select("img[data-src*='channels']")
            channel_names = []
            for channel_tag in channel_tags:
                channel_name = channel_tag.get("title", "").strip()
                if channel_name:  # Eğer kanal adı varsa ekleyelim
                    channel_names.append(channel_name)
            
            # Kanal adı 'TUTTUR TV' ise bir sonraki kanal bilgisini alalım
            for i in range(len(channel_names)):
                if channel_names[i].upper() == "TUTTUR TV" and i + 1 < len(channel_names):
                    # 'TUTTUR TV' bulunduysa, bir sonraki kanal ismini alıyoruz
                    main_channel = channel_names[i + 1]
                    break
            else:
                # Eğer 'TUTTUR TV' bulunmazsa, ilk kanal alınır
                main_channel = channel_names[0] if channel_names else "Bulunamadı"
            
            # 'TUTTUR TV' ise 'NBA TV' olarak değiştir
            if main_channel.upper() == "TUTTUR TV":
                main_channel = "NBA TV"
            # 'TUTTUR TV' ise 'S SPORT PLUS' olarak değiştir
            if main_channel.upper() == "S SPORT PLUS":
                main_channel = "SARAN SPORT 2"
            
            # Sıralama: Maç Adı, Saat, Kanal, Logo URL
            output = f"MAÇ ADI= {match_name.upper()}\nSAAT= {match_time.upper()}\nKANAL= {main_channel.upper()}\nLOGO URL= {logo_url}\n\n"
            file.write(output)

scrape_sporekrani()
