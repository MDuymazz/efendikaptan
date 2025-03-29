from bs4 import BeautifulSoup
import requests

# Veriyi çekeceğimiz temel URL
base_url = "https://tvplus.com.tr/canli-tv/yayin-akisi/bugun-hangi-belgeseller-var"

# Sonuçları saklamak için liste
results = []

response = requests.get(base_url)
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
    if channel == "NATIONAL GEOGRAPHIC WILD":
        channel = "NAT GEO WILD"

    # Logo URL
    logo_url = dizi.find('div', class_='channel-epg-link').find('img')['src']

    # Formatlı veri oluşturma
    output = f"""
MAÇ ADI= {match_name} 
SAAT= {time}
KANAL= {channel}
LOGO URL= {logo_url}
"""

    results.append(output)

# Verileri diziler.txt dosyasına kaydetme
with open("belgesel.txt", "w", encoding="utf-8") as file:
    file.writelines(results)

print("Bugünün belgeseller belgesel.txt dosyasına kaydedildi.")
