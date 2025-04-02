# M3U dosyasındaki verileri oku (group-title="TURKEY" ve group-title="SPOR YAYINLARI" olanları al)
def read_m3u_file(m3u_file):
    channels = []
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if 'group-title="TURKEY"' in line or 'group-title="SPOR YAYINLARI"' in line or 'group-title="BELGESEL YAYINLARI"' in line or 'group-title="SİNEMA YAYINLARI"' in line:
            channel_info = {}
            parts = line.split('tvg-name="')
            if len(parts) > 1:
                channel_info["name"] = parts[1].split('"')[0]  # Kanal adı
            
            # URL'nin 4. satırda olduğundan emin ol
            if i + 3 < len(lines):
                channel_info["url"] = lines[i + 3].strip()  # URL satırı
                
            channels.append(channel_info)
        i += 1
    
    return channels


# TUR bilgilerine göre veri dosyasındaki maçları oku
def read_tur_data(veri_file):
    tur_matches = {}  # Dinamik olarak kategoriler eklenecek
    current_tur = None

    with open(veri_file, 'r', encoding='utf-8') as f:
        match_info = {}
        for line in f:
            line = line.strip()
            if line.startswith("TUR="):  # TUR başlığına göre kategori değiştir
                current_tur = line.split("=")[1].strip()
                if current_tur not in tur_matches:
                    tur_matches[current_tur] = []  # Yeni kategori oluştur
            elif line.startswith("MAÇ ADI="):
                match_info["name"] = line.split("=")[1].strip()
            elif line.startswith("SAAT="):
                match_info["time"] = line.split("=")[1].strip()
            elif line.startswith("KANAL="):
                match_info["channel"] = line.split("=")[1].strip()
            elif line.startswith("LOGO URL="):
                match_info["logo"] = line.split("=")[1].strip()
                if current_tur:
                    tur_matches[current_tur].append(match_info)
                match_info = {}  # Yeni maç için sıfırla
    
    return tur_matches

# TUR verilerine göre yeni M3U dosyası oluştur
def create_new_m3u_for_tur(m3u_channels, tur_matches, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")  # M3U dosyasının başlığı

        # Her TUR kategorisini işle
        for tur_category, matches in tur_matches.items():
            for match in matches:
                for channel in m3u_channels:
                    if match["channel"] == channel["name"]:  # Kanal eşleşmesi
                        # MAÇ ADI ve SAAT bilgisini yan yana ekle
                        f.write(f'#EXTINF:-1 tvg-id="None" tvg-name="{channel["name"]}" '
                                f'tvg-logo="{match["logo"]}" group-title="{tur_category}", '
                                f'{match["time"]} {match["name"]}\n')
                        f.write('#EXTVLCOPT:http-user-agent=VAVOO/1.0\n')
                        f.write('#EXTVLCOPT:http-referrer=https://vavoo.to/\n')
                        f.write(f'{channel["url"]}\n\n')


# Dosya yolları
m3u_file = 'vavoo.m3u'
veri_file = 'programlar.txt'
output_file = 'programlar.m3u'  # Çıktı dosyası adı

# M3U ve veri dosyalarını oku
m3u_channels = read_m3u_file(m3u_file)
tur_matches = read_tur_data(veri_file)

# Yeni M3U dosyasını TUR kategorilerine göre oluştur
create_new_m3u_for_tur(m3u_channels, tur_matches, output_file)

print(f"Yeni M3U dosyası '{output_file}' olarak oluşturuldu.")
