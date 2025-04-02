from bs4 import BeautifulSoup
import requests
from datetime import datetime

# URL'ler ve başlık eşleşmeleri
type_mappings = {
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-diziler-var": "BUGÜNÜN DİZİLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-filmler-var": "BUGÜNÜN FİLMLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-spor-icerikleri-var": "BUGÜNÜN SPOR İÇERİKLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-belgeseller-var": "BUGÜNÜN BELGESELLERİ",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-haber-programlari-var": "BUGÜNÜN HABER PROGRAMLARI"
}

# Sonuçları saklamak için sözlük
type_results = {title: [] for title in type_mappings.values()}

for base_url, title in type_mappings.items():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tüm program öğelerini bulma
    program_listesi = soup.find_all('li', class_='playbill-list-item')

    for program in program_listesi:
        # Program adı
        match_name = program.find('h3').text.strip().upper()

        # Saat bilgisi
        time_full = program.find('time').text.strip()
        time_sort = time_full.split(' - ')[0]  # Sıralama için sadece başlangıç saati alınır

        # Kanal adı
        channel = program.find('span', class_='channel-detail-link').text.strip()

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
            "HABERTÜRK": "HABERTURK"
        }
        channel = channel_mappings.get(channel, channel)

        # Logo URL
        logo_url = program.find('div', class_='channel-epg-link').find('img')['src']

        # Formatlı veri oluşturma
        output = {
            "name": match_name,
            "time": time_full,  # Orijinal saat bilgisi korunuyor
            "time_sort": time_sort,  # Sadece sıralama için kullanılacak saat
            "channel": channel,
            "logo_url": logo_url
        }

        type_results[title].append(output)

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
