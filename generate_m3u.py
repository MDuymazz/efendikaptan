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
    
    sporyayinlari_channels = []  # SPOR YAYINLARI kanallarını tutacağımız liste
    belge_channel = []  # BELGESEL YAYINLARI kanallarını tutacağımız liste
    sinema_channel = []  # SİNEMA YAYINLARI kanallarını tutacağımız liste
    other_channels = []  # Diğer kanallar için bir liste

    for first_letter in sorted(grouped_channels.keys()):
        for country, channel_name, button_id_url in grouped_channels[first_letter]:
            clean_channel_name = channel_name.replace('"', '')
            
            # Sadece "Turkey" için "SPOR YAYINLARI" ekliyoruz
            if country.upper() == "TURKEY" and ("TABII" in channel_name or "SPOR" in channel_name or "EXXEN" in channel_name):
                group_title = "SPOR YAYINLARI"
                sporyayinlari_channels.append((clean_channel_name, group_title, button_id_url))
            # Turkey için "BELGESEL YAYINLARI" ekliyoruz, diğer anahtar kelimelerle birlikte
            elif country.upper() == "TURKEY" and any(keyword in channel_name.upper() for keyword in ["BELGESEL", "DOKÜMANTER", "NATGEO", "DISCOVERY", "GEOGRAPHIC", "WILD"]):
                group_title = "BELGESEL YAYINLARI"
                belge_channel.append((clean_channel_name, group_title, button_id_url))
            # Turkey için "SİNEMA YAYINLARI" ekliyoruz, diğer anahtar kelimelerle birlikte
            elif country.upper() == "TURKEY" and any(keyword in channel_name.upper() for keyword in ["SİNEMA", "MOVIE", "FILM"]):
                group_title = "SİNEMA YAYINLARI"
                sinema_channel.append((clean_channel_name, group_title, button_id_url))
            # "BELGESEL", "DOKÜMANTER", "NATGEO", "DISCOVERY" içeren kanallar için "BELGESEL YAYINLARI" ekliyoruz
            elif any(keyword in channel_name.upper() for keyword in ["BELGESEL", "DOKÜMANTER", "NATGEO", "DISCOVERY", "GEOGRAPHIC", "WILD"]):
                group_title = "BELGESEL YAYINLARI"
                belge_channel.append((clean_channel_name, group_title, button_id_url))
            # "SİNEMA", "MOVIE", "FILM" içeren kanallar için "SİNEMA YAYINLARI" ekliyoruz
            elif any(keyword in channel_name.upper() for keyword in ["SİNEMA", "MOVIE", "FILM", "SINEMA"]):
                group_title = "SİNEMA YAYINLARI"
                sinema_channel.append((clean_channel_name, group_title, button_id_url))
            else:
                group_title = country.upper()  # Diğer ülkeler için normal ülke adı
                other_channels.append((clean_channel_name, group_title, button_id_url))

    # SPOR YAYINLARI olan kanalları, tvg-name'in ilk 5 harfine göre sıralıyoruz
    sporyayinlari_channels.sort(key=lambda x: x[0][:5].upper())

    # BELGESEL YAYINLARI olan kanalları, tvg-name'in ilk 5 harfine göre sıralıyoruz
    belge_channel.sort(key=lambda x: x[0][:5].upper())

    # SİNEMA YAYINLARI olan kanalları, tvg-name'in ilk 5 harfine göre sıralıyoruz
    sinema_channel.sort(key=lambda x: x[0][:5].upper())

    # SPOR YAYINLARI kanallarını yazma
    for clean_channel_name, group_title, button_id_url in sporyayinlari_channels:
        m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n
"""
        output.write(m3u_content)

    # BELGESEL YAYINLARI kanallarını yazma
    for clean_channel_name, group_title, button_id_url in belge_channel:
        m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n
"""
        output.write(m3u_content)

    # SİNEMA YAYINLARI kanallarını yazma
    for clean_channel_name, group_title, button_id_url in sinema_channel:
        m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n
"""
        output.write(m3u_content)

    # Diğer kanalları yazma
    for clean_channel_name, group_title, button_id_url in other_channels:
        m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n
"""
        output.write(m3u_content)

print(f"{output_file} dosyası başarıyla oluşturuldu.")
