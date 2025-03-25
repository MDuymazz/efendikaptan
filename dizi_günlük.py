from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Haftalık dizi listesi için günler
gunler = {
    "monday": "pazartesi-dizileri",
    "tuesday": "sali-dizileri",
    "wednesday": "carsamba-dizileri",
    "thursday": "persembe-dizileri",
    "friday": "cuma-dizileri",
    "saturday": "cumartesi-dizileri",
    "sunday": "pazar-dizileri"
}

# Bugünün gününü al (İngilizce)
bugun_gun = datetime.now().strftime("%A").lower()

# Eğer bugünün adı listede varsa, o günün dizilerini al
if bugun_gun in gunler:
    gun = gunler[bugun_gun]
else:
    print(f"Bugün için geçerli bir gün bulunamadı: {bugun_gun}")
    exit()

base_url = "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-diziler-var/"

# Sonuçları saklamak için liste
results = []

url = base_url + gun
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Tüm dizi öğelerini bulma
dizi_listesi = soup.find_all('li', class_='playbill-list-item')

for dizi in dizi_listesi:
    # Dizi adı
    match_name = dizi.find('h3').text.strip().upper()

    # Saat bilgisi
    time = dizi.find('time').text.strip()

    # Kanal adı
    channel = dizi.find('span', class_='channel-detail-link').text.strip()

    # "KANAL= NOW" ise "KANAL= NOW TV HD" olarak değiştir
    if channel == "NOW":
        channel = "NOW TV HD"
    if channel == "TRT1":
        channel = "TRT 1"

    # Logo URL
    logo_url = dizi.find('div', class_='channel-epg-link').find('img')['src']

    # Gün bilgisini başına ekleyerek format oluşturma
    output = f"""
MAÇ ADI= {match_name} 
SAAT= {time}
KANAL= {channel}
LOGO URL= {logo_url}
"""

    results.append(output)

# Verileri diziler.txt dosyasına kaydetme
with open("diziler.txt", "w", encoding="utf-8") as file:
    file.writelines(results)

print(f"Bugün {bugun_gun.upper()} günü için veriler diziler.txt dosyasına kaydedildi.")
