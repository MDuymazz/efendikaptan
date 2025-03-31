# M3U dosyasındaki verileri oku (group-title="TURKEY" ve group-title="SPOR YAYINLARI" olanları al)
def read_m3u_file(m3u_file):
    channels = []
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        channel_info = {}
        url = ""
        for line in lines:
            if 'group-title' in line and ('TURKEY' in line or 'SPOR YAYINLARI' in line):  # Daha genel kontrol
                # Kanal adı ve diğer bilgileri al
                parts = line.split("tvg-name=")
                channel_info["name"] = parts[1].split('"')[1]  # Kanal adı
                # URL'nin bulunduğu satır, her zaman 4. satırda (sonuncu satır)
                url = lines[lines.index(line) + 3].strip()  # Stream URL
                channel_info["url"] = url
                channel_info["group_title"] = "GÜNLÜK SPOR AKIŞI"  # group-title her zaman SPOR EKRANI olacak
                channels.append(channel_info)
                channel_info = {}
    return channels


# Veri dosyasındaki maç bilgilerini oku (TÜM maçları al)
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
                match_info["channel"] = line.split("=")[1].strip()  # Tüm kanalları al
            elif "LOGO URL=" in line:
                match_info["logo"] = line.split("=")[1].strip()
                matches.append(match_info)
                match_info = {}  # Yeni maç için sıfırla
    return matches


# Yeni M3U dosyasını oluştur
def create_new_m3u(m3u_channels, match_details, output_file):
    # Saat bilgisine göre sıralama yap
    match_details_sorted = sorted(match_details, key=lambda x: x["time"])  # Saat bilgisine göre sıralama

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")  # Dosyanın en başına #EXTM3U ekleniyor

        # Her kanal ve maç kombinasyonu için kontrol edilen bir set oluşturuyoruz
        written_matches = set()

        for match in match_details_sorted:
            for channel in m3u_channels:
                # Kanal adı tam eşleşme ile kontrol ediliyor (Küçük harfe dönüştürülmüş eşleşme)
                if match["channel"].lower() == channel["name"].lower():
                    # Kanal adı ve maç adı kombinasyonunu kontrol et
                    match_key = (match["channel"].lower(), match["name"].lower())
                    if match_key not in written_matches:
                        # Yeni M3U formatında yaz: "00:00 NAME (CHANNEL)"
                        f.write(f'#EXTINF:-1 tvg-id="None" tvg-name="{channel["name"]}" tvg-logo="{match["logo"]}" '
                                f'group-title="{channel["group_title"]}", {match["time"]} {match["name"]} ({match["channel"]})\n')
                        f.write('#EXTVLCOPT:http-user-agent=VAVOO/1.0\n')
                        f.write('#EXTVLCOPT:http-referrer=https://vavoo.to/\n')
                        f.write(f'{channel["url"]}\n')
                        f.write("\n")
                        # Yazıldığını kaydet
                        written_matches.add(match_key)


# Dosya yolları
m3u_file = 'vavoo.m3u'
veri_file = 'veri.txt'
output_file = 'new_m3u.m3u'

# M3U ve veri dosyalarını oku
m3u_channels = read_m3u_file(m3u_file)
match_details = read_veri_txt(veri_file)

# Yeni M3U dosyasını oluştur
create_new_m3u(m3u_channels, match_details, output_file)

print(f"Yeni m3u dosyası '{output_file}' olarak oluşturuldu.")
