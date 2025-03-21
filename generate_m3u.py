import re
from collections import defaultdict

# Dosya adları
input_file = "all_countries_channels.txt"
output_file = "vavoo.m3u"
temp_turkey_file = "turkey_temp.m3u"  # Turkey kanalları için geçici dosya

# Kanal bilgilerini gruplamak için liste oluşturuyoruz
channels = []

# Dosyayı okuma
with open(input_file, "r", encoding="utf-8") as file:
    country = None
    channel_name = None
    button_id_url = None
    
    for line in file:
        if line.startswith("Country = "):
            country = line.split('=')[1].strip().strip('"')
        elif line.startswith("Channel Name: "):
            channel_name = line.replace("Channel Name: ", "").strip().strip('"')
            channel_name = re.sub(r"\(.*?\)", "", channel_name).strip()  # Parantez içindeki veriyi temizle
        elif line.startswith("Button ID URL: "):
            button_id_url = line.split(':', 1)[1].strip().strip('"')
            
            if country and channel_name and button_id_url:
                channels.append((country, channel_name, button_id_url))
                country = channel_name = button_id_url = None  # Verileri sıfırlıyoruz

# tvg-name değerine göre ilk 11 harf baz alınarak sıralama
channels.sort(key=lambda x: x[1][:14].upper())

# Öncelikli gruplar
priority_groups = ["SPOR YAYINLARI", "BELGESEL YAYINLARI", "SİNEMA YAYINLARI", "TURKEY"]
priority_channels = []
other_channels = []

# Kanalları gruplandırma
for country, channel_name, button_id_url in channels:
    clean_channel_name = channel_name.replace('"', '')
    if country.upper() == "TURKEY":
        # Turkey için özel işlemler
        if "TABII" in channel_name or "SPOR" in channel_name or "EXXEN" in channel_name:
            group_title = "SPOR YAYINLARI"
        elif any(keyword in channel_name.upper() for keyword in ["BELGESEL", "DOKÜMANTER", "NATGEO", "DISCOVERY", "GEOGRAPHIC", "WILD"]):
            group_title = "BELGESEL YAYINLARI"
        elif any(keyword in channel_name.upper() for keyword in ["SİNEMA", "MOVIE", "FILM"]):
            group_title = "SİNEMA YAYINLARI"
        else:
            group_title = "TURKEY"
    else:
        group_title = country.upper()
    
    m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n
"""
    
    if group_title in priority_groups:
        priority_channels.append(m3u_content)
    else:
        other_channels.append(m3u_content)

# M3U dosyasını oluşturma
with open(output_file, "w", encoding="utf-8") as output:
    output.write("#EXTM3U\n\n\n")
    
    # Öncelikli grupları önce yaz
    output.writelines(priority_channels)
    
    # Diğer kanalları ekle
    output.writelines(other_channels)

print(f"{output_file} dosyası başarıyla oluşturuldu ve öncelikli gruplar en başta olacak şekilde sıralandı.")
