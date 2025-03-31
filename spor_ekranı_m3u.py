# M3U dosyasındaki verileri oku (group-title belirli olanları al)
def read_m3u_file(m3u_file):
    channels = {}
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if 'group-title="TURKEY"' in line or 'group-title="SPOR YAYINLARI"' in line or 'group-title="BELGESEL YAYINLARI"' in line or 'group-title="SİNEMA YAYINLARI"' in line:
            parts = line.split('tvg-name="')
            if len(parts) > 1:
                channel_name = parts[1].split('"')[0]  # Kanal adı
                
                if channel_name not in channels:
                    channels[channel_name] = {
                        "name": channel_name,
                        "group_title": "GÜNLÜK TELEVİZYON AKIŞI",
                        "urls": []  # Birden fazla URL saklamak için liste
                    }
                
                # URL ekleyelim
                if i + 3 < len(lines):
                    url = lines[i + 3].strip()
                    if url not in channels[channel_name]["urls"]:  # Aynı URL tekrar eklenmesin
                        channels[channel_name]["urls"].append(url)
        i += 1
    
    return list(channels.values())  # Kanal listesini tekil hale getirip döndür


# Veri dosyasındaki maç bilgilerini oku (Sıra bozulmadan)
def read_veri_txt(veri_file):
    matches = []
    match_info = {}
    
    with open(veri_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("MAÇ ADI="):
                match_info["name"] = line.split("=")[1].strip()
            elif line.startswith("SAAT="):
                match_info["time"] = line.split("=")[1].strip()
            elif line.startswith("KANAL="):
                match_info["channel"] = line.split("=")[1].strip()
            elif line.startswith("LOGO URL="):
                match_info["logo"] = line.split("=")[1].strip()
                matches.append(match_info)
                match_info = {}  # Yeni maç için sıfırla
    
    return matches


# Yeni M3U dosyasını oluştur (Diziler.txt sırasını koruyarak)
def create_new_m3u(m3u_channels, match_details, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")  # M3U başlığı
        
        for match in match_details:
            for channel in m3u_channels:
                if match["channel"] == channel["name"]:  # Kanal eşleşmesi
                    # Maç bilgilerini içeren EXTINF satırını yaz
                    f.write(f'#EXTINF:-1 tvg-id="None" tvg-name="{channel["name"]}" '
                            f'tvg-logo="{match["logo"]}" group-title="{channel["group_title"]}", '
                            f'{match["time"]} {match["name"]}\n')
                    f.write('#EXTVLCOPT:http-user-agent=VAVOO/1.0\n')
                    f.write('#EXTVLCOPT:http-referrer=https://vavoo.to/\n')

                    # **Tüm URL’leri sırayla yaz**
                    for url in channel["urls"]:
                        f.write(f'{url}\n')

                    f.write("\n")  # Yeni satır ekleyerek bir sonraki girişe geç


# Dosya yolları
m3u_file = 'vavoo.m3u'
veri_file = 'programlar.txt'
output_file = 'programlar.m3u'

# M3U ve veri dosyalarını oku
m3u_channels = read_m3u_file(m3u_file)
match_details = read_veri_txt(veri_file)

# Yeni M3U dosyasını oluştur (Sıra bozulmadan)
create_new_m3u(m3u_channels, match_details, output_file)

print(f"Yeni M3U dosyası '{output_file}' olarak oluşturuldu.")
