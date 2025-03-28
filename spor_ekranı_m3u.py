from datetime import datetime

# M3U dosyasındaki verileri oku (group-title="TURKEY" ve group-title="SPOR YAYINLARI" olanları al)
def read_m3u_file(m3u_file):
    channels = []
    
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if 'group-title="TURKEY"' in line or 'group-title="SPOR YAYINLARI"' in line:
            channel_info = {}

            # Kanal adını al
            parts = line.split('tvg-name="')
            if len(parts) > 1:
                channel_info["name"] = parts[1].split('"')[0]

            # URL'yi al (her zaman bir sonraki satır)
            if i + 1 < len(lines):
                channel_info["url"] = lines[i + 1].strip()

            channel_info["group_title"] = "GÜNLÜK SPOR AKIŞI"  # Sabit grup başlığı

            channels.append(channel_info)
        
        i += 1  # Bir sonraki satıra geç
    
    return channels


# Veri dosyasındaki maç bilgilerini oku (TÜM maçları al, filtreleme yapma)
def read_veri_txt(veri_file):
    matches = []
    match_info = {}

    with open(veri_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if "MAÇ ADI=" in line:
            match_info["name"] = line.split("=")[1].strip()
        elif "SAAT=" in line:
            match_info["time"] = line.split("=")[1].strip()
        elif "KANAL=" in line:
            match_info["channel"] = line.split("=")[1].strip()  # TÜM kanalları listeye ekle
        elif "LOGO URL=" in line:
            if match_info:  # Geçerli bir maç varsa
                match_info["logo"] = line.split("=")[1].strip()
                matches.append(match_info)
                match_info = {}  # Yeni maç için sıfırla

    return matches


# Yeni M3U dosyasını oluştur
def create_new_m3u(m3u_channels, match_details, output_file):
    # Saat bilgisine göre sıralama yap (HH:MM formatına göre)
    match_details_sorted = sorted(match_details, key=lambda x: datetime.strptime(x["time"], "%H:%M"))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")

        for match in match_details_sorted:
            for channel in m3u_channels:
                if match["channel"] == channel["name"]:  # Kanal adı eşleşirse
                    f.write(f'#EXTINF:-1 tvg-id="None" tvg-name="{channel["name"]}" tvg-logo="{match["logo"]}" '
                            f'group-title="{channel["group_title"]}", {match["time"]} {match["name"]} ({match["channel"]})\n')
                    f.write('#EXTVLCOPT:http-user-agent=VAVOO/1.0\n')
                    f.write('#EXTVLCOPT:http-referrer=https://vavoo.to/\n')
                    f.write(f'{channel["url"]}\n\n')


# Dosya yolları
m3u_file = 'vavoo.m3u'
veri_file = 'veri.txt'
output_file = 'new_m3u.m3u'

# M3U ve veri dosyalarını oku
m3u_channels = read_m3u_file(m3u_file)
match_details = read_veri_txt(veri_file)

# Yeni M3U dosyasını oluştur
create_new_m3u(m3u_channels, match_details, output_file)

print(f"Yeni M3U dosyası '{output_file}' olarak oluşturuldu.")
