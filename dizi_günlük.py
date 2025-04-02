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

# Sonuçları saklamak için sözlük
type_results = {title: [] for title in type_mappings.values()}

def parse_date(date_text, time_text):
    try:
        date_obj = datetime.strptime(date_text + " " + time_text, "%d %B %H:%M")
        return date_obj.strftime("%Y-%m-%d %H:%M"), date_obj
    except ValueError:
        return f"{date_text} {time_text}", datetime.max

for base_url, title in type_mappings.items():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if "futbol-fiksturu" in base_url or "basketbol-fiksturu" in base_url:
        fixture_days = soup.find_all('div', class_='fixture-day')
        for day in fixture_days:
            date_text = day.find('h3', class_='fixture-day-title').text.strip().upper()
            program_listesi = day.find_all('li', class_='fixture-day-list-item')
            for program in program_listesi:
                time_full = program.find('span', class_='start-time').text.strip()
                time_sort, date_obj = parse_date(date_text, time_full)
                match_name = program.find('a', class_='match-name').find('span').text.strip().upper()
                channel_element = program.find_all('a')[-1]
                channel = channel_element.get('title', '').replace(' İzle', '').strip()
                logo_img = channel_element.find('img')
                logo_url = logo_img['src'] if logo_img else ''
                
                type_results[title].append({
                    "name": match_name,
                    "time": f"{date_text} {time_full}",
                    "time_sort": date_obj,
                    "channel": channel,
                    "logo_url": logo_url
                })
    else:
        program_listesi = soup.find_all('li', class_='playbill-list-item')
        for program in program_listesi:
            match_name = program.find('h3').text.strip().upper()
            time_full = program.find('time').text.strip()
            time_sort, date_obj = parse_date(datetime.now().strftime("%d %B"), time_full.split(' - ')[0])
            channel = program.find('span', class_='channel-detail-link').text.strip()
            logo_url = program.find('div', class_='channel-epg-link').find('img')['src']
            
            type_results[title].append({
                "name": match_name,
                "time": time_full,
                "time_sort": date_obj,
                "channel": channel,
                "logo_url": logo_url
            })

# Verileri programlar.txt dosyasına kaydetme
with open("programlar.txt", "w", encoding="utf-8") as file:
    for category, programs in type_results.items():
        file.write(f"\nTUR= {category}\n")
        if programs:
            programs.sort(key=lambda x: x['time_sort'])
            for result in programs:
                output = f"MAÇ ADI= {result['name']}\nSAAT= {result['time']}\nKANAL= {result['channel']}\nLOGO URL= {result['logo_url']}\n\n"
                file.write(output)

print("Programlar tarih ve saat sırasına göre programlar.txt dosyasına kaydedildi.")
