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
            parts = line.split('tvg-name="')
            if len(parts) > 1:
                channel_info["name"] = parts[1].split('"')[0]  # Kanal adı
            
            # URL'nin 4. satırda olduğundan emin ol
            if i + 3 < len(lines):
                channel_info["url"] = lines[i + 3].strip()  # URL satırı
                
            channel_info["group_title"] = "GÜNLÜK DİZİ PROGRAMI"  # Tüm kanallar aynı grup olacak
            channels.append(channel_info)
        i += 1
    
    return channels


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
        f.write("#EXTM3U\n\n")  # M3U dosyasının başlığı
        
        for match in match_details:
            for channel in m3u_channels:
                if match["channel"] == channel["name"]:  # Kanal eşleşmesi
                    # MAÇ ADI ve SAAT bilgisini yan yana ekle
                    f.write(f'#EXTINF:-1 tvg-id="None" tvg-name="{channel["name"]}" '
                            f'tvg-logo="{match["logo"]}" group-title="{channel["group_title"]}", '
                            f'{match["time"]} {match["name"]}\n')
                    f.write('#EXTVLCOPT:http-user-agent=VAVOO/1.0\n')
                    f.write('#EXTVLCOPT:http-referrer=https://vavoo.to/\n')
                    f.write(f'{channel["url"]}\n\n')  # URL doğru şekilde yazılacak


# Dosya yolları
m3u_file = 'vavoo.m3u'
veri_file = 'diziler.txt'
output_file = 'diziler.m3u'

# M3U ve veri dosyalarını oku
m3u_channels = read_m3u_file(m3u_file)
match_details = read_veri_txt(veri_file)

# Yeni M3U dosyasını oluştur (Sıra bozulmadan)
create_new_m3u(m3u_channels, match_details, output_file)

print(f"Yeni M3U dosyası '{output_file}' olarak oluşturuldu.")
