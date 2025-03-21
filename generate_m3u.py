import re
from collections import defaultdict

# Dosya adları
input_file = "all_countries_channels.txt"
output_file = "vavoo.m3u"

# Kanal bilgilerini gruplamak için sözlük oluşturuyoruz
grouped_channels = defaultdict(list)

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
                first_letter = channel_name[0].upper()  # İlk harfi alıp büyük harfe çeviriyoruz
                grouped_channels[first_letter].append((country, channel_name, button_id_url))
                country = channel_name = button_id_url = None  # Verileri sıfırlıyoruz

# M3U dosyasını oluşturma
with open(output_file, "w", encoding="utf-8") as output:
    output.write("#EXTM3U\n\n\n")
    
    for first_letter in sorted(grouped_channels.keys()):
        for country, channel_name, button_id_url in grouped_channels[first_letter]:
            clean_channel_name = channel_name.replace('"', '')
            
            # Normal group-title (ülke adı)
            group_title = country.upper()

            # Sadece "Turkey" için "SPOR YAYINLARI" ekliyoruz
            if country.upper() == "TURKEY" and ("TABII" in channel_name or "SPOR" in channel_name or "EXXEN" in channel_name or "BEIN" in channel_name):
                group_title_with_sport = f"{group_title} | SPOR YAYINLARI"
            else:
                group_title_with_sport = group_title
            
            m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n

#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{group_title_with_sport}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n
"""
            output.write(m3u_content)

print(f"{output_file} dosyası başarıyla oluşturuldu.")
