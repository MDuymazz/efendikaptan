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
    "tabii spor": "TABII SPOR HD",
    "TV8,5": "TV 8.5 HD"
}

# Türkçe ay adlarını İngilizce'ye dönüştürme
month_translation = {
    "OCAK": "January",
    "ŞUBAT": "February",
    "MART": "March",
    "NISAN": "April",
    "MAYIS": "May",
    "HAZIRAN": "June",
    "TEMMUZ": "July",
    "AGUSTOS": "August",
    "EYLUL": "September",
    "EKIM": "October",
    "KASIM": "November",
    "ARALIK": "December"
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
                time_sort = f"{date_text} {time_full}"  # Tarih ve saat birlikte sıralama için kullanılır
                match_name = program.find('a', class_='match-name').find('span').text.strip().upper()
                # Broadcast türünü al
                broadcast_type = program.find('i', class_='match-broadcast-type')
                if broadcast_type:
                    broadcast_text = broadcast_type.text.strip()
                    match_name = f"{match_name}({broadcast_text.upper()})"
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
            # Tarih ve saat sırasına göre sıralama
            for program in programs:
                # Türkçe ay adlarını İngilizce'ye çevir
                for turkish_month, english_month in month_translation.items():
                    program['time_sort'] = program['time_sort'].replace(turkish_month, english_month)
                
                # Handle cases where the time is only the time (e.g., '00:45')
                if len(program['time_sort'].split()) == 1:  # Only time present
                    # Add a default date and month (for example, use '01 January')
                    program['time_sort'] = f"01 January {program['time_sort']}"

            # Tarih ve saat sırasına göre sıralama
            programs.sort(key=lambda x: datetime.strptime(x['time_sort'], '%d %B %H:%M'))  # Gün, Ay, Saat: Dakika sıralaması
            for result in programs:
                output = f"MAÇ ADI= {result['name']}\nSAAT= {result['time']}\nKANAL= {result['channel']}\nLOGO URL= {result['logo_url']}\n\n"
                file.write(output)

print("Bugünün programları tarih ve saat sırasına göre programlar.txt dosyasına kaydedildi.")
