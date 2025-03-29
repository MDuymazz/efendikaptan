from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Veriyi çekeceğimiz URL'ler
urls = [
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-diziler-var",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-filmler-var",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-spor-icerikleri-var",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-belgeseller-var",
    "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-haber-programlari-var"
]

# Sonuçları saklamak için liste
results = []

for base_url in urls:
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

        results.append(output)

# Saatlere göre sıralama
results.sort(key=lambda x: datetime.strptime(x['time_sort'], '%H:%M'))

# Verileri programlar.txt dosyasına kaydetme
with open("programlar.txt", "w", encoding="utf-8") as file:
    for result in results:
        output = f"""
MAÇ ADI= {result['name']}
SAAT= {result['time']}
KANAL= {result['channel']}
LOGO URL= {result['logo_url']}
"""
        file.write(output)

print("Bugünün programları saat sırasına göre programlar.txt dosyasına kaydedildi.")
