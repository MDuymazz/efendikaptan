from bs4 import BeautifulSoup
import requests
from datetime import datetime

# URL'ler ve başlık eşleşmeleri
type_mappings = {
    "https://tvplus.com.tr/canli-tv/yayin-akisi/tvdebugun-futbol-fiksturu": "HAFTANIN FUTBOL FİKSTÜRÜ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/tvdebugun-basketbol-fiksturu": "HAFTANIN BASKETBOL FİKSTÜRÜ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-diziler-var": "BUGÜNÜN DİZİLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-filmler-var": "BUGÜNÜN FİLMLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-spor-icerikleri-var": "BUGÜNÜN SPOR İÇERİKLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-belgeseller-var": "BUGÜNÜN BELGESELLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-haber-programlari-var": "BUGÜNÜN HABER PROGRAMLARI"
}

# Kanal adı dönüşümleri
channel_mappings = {
    "NOW": "NOW TV HD",
    "TRT1": "TRT 1",
    "SİNEMA YERLİ": "SINEMA YERLI 1",
    "NATIONAL GEOGRAPHIC WILD": "NAT GEO WILD",
    "CNN TÜRK": "CNN TURK",
    "SÖZCÜ TV": "SZC",
    "SİNEMA AİLE": "SINEMA AILE 1",
    "SİNEMA TV": "SINEMA TV",
    "HABERTÜRK": "HABERTURK",
    "tabii spor": "TABII SPOR 1 720P"

}

# Sonuçları saklamak için sözlük
type_results = {title: [] for title in type_mappings.values()}

for base_url, title in type_mappings.items():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Farklı HTML yapıları için uygun CSS seçicileri belirleme
    if "futbol-fiksturu" in base_url or "basketbol-fiksturu" in base_url:
        fixture_days = soup.find_all('div', class_='fixture-day')
        for day in fixture_days:
            date_text = day.find('h3', class_='fixture-day-title').text.strip().upper()
            program_listesi = day.find_all('li', class_='fixture-day-list-item')
            for program in program_listesi:
                time_full = program.find('span', class_='start-time').text.strip()
                time_sort = time_full
                match_name = program.find('a', class_='match-name').find('span').text.strip().upper()
                channel_element = program.find_all('a')[-1]
                channel = channel_element.get('title', '').replace(' İzle', '').strip()
                channel = channel_mappings.get(channel, channel)  # Kanal adı dönüşümü
                logo_img = channel_element.find('img')
                logo_url = logo_img['src'] if logo_img else ''
                
                type_results[title].append({
                    "name": match_name,
                    "time": f"{date_text} {time_full}",
                    "time_sort": time_sort,
                    "channel": channel,
                    "logo_url": logo_url
                })
    else:
        program_listesi = soup.find_all('li', class_='playbill-list-item')
        for program in program_listesi:
            match_name = program.find('h3').text.strip().upper()
            time_full = program.find('time').text.strip()
            time_sort = time_full.split(' - ')[0]
            channel = program.find('span', class_='channel-detail-link').text.strip()
            channel = channel_mappings.get(channel, channel)  # Kanal adı dönüşümü
            logo_url = program.find('div', class_='channel-epg-link').find('img')['src']
            
            type_results[title].append({
                "name": match_name,
                "time": time_full,
                "time_sort": time_sort,
                "channel": channel,
                "logo_url": logo_url
            })

# Verileri programlar.txt dosyasına kaydetme
with open("programlar.txt", "w", encoding="utf-8") as file:
    for category, programs in type_results.items():
        file.write(f"\nTUR= {category}\n")
        if programs:
            programs.sort(key=lambda x: datetime.strptime(x['time_sort'], '%H:%M'))
            for result in programs:
                output = f"MAÇ ADI= {result['name']}\nSAAT= {result['time']}\nKANAL= {result['channel']}\nLOGO URL= {result['logo_url']}\n\n"
                file.write(output)

print("Bugünün programları saat sırasına göre programlar.txt dosyasına kaydedildi.")
