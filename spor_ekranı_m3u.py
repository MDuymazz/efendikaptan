# M3U dosyasındaki verileri oku (group-title="TURKEY" ve group-title="SPOR YAYINLARI" olanları al)
def read_m3u_file(m3u_file):
    channels = []
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        channel_info = {}
        url = ""
        for line in lines:
            if 'group-title="TURKEY"' in line or 'group-title="SPOR YAYINLARI"' in line:  # İki group-title'ı kontrol et
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
                # Eğer kanal zaten varsa, onu listeye ekleyelim
                if "channels" not in match_info:
                    match_info["channels"] = []
                match_info["channels"].append(line.split("=")[1].strip())  # Kanal adı
            elif "LOGO URL=" in line:
                match_info["logo"] = line.split("=")[1].strip()
                # Maç verisini kaydet, kanal bilgilerini de liste olarak ekleyelim
                matches.append(match_info)
                match_info = {}  # Yeni maç için sıfırla
    return matches


# Yeni M3U dosyasını oluştur
def create_new_m3u(m3u_channels, match_details, output_file):
    # Saat bilgisine göre sıralama yap
    match_details_sorted = sorted(match_details, key=lambda x: x["time"])  # Saat bilgisine göre sıralama

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")  # Dosyanın en başına #EXTM3U ekleniyor
        
        # Kanal başına yalnızca bir kez yazma
        written_channels = set()

        for match in match_details_sorted:
            match_found = False  # Bu maç için eşleşen kanal bulup bulmadığımızı takip etmek için
            for channel in m3u_channels:
                for match_channel in match["channels"]:  # Bir maç birden fazla kanala sahip olabilir
                    # Kanal adı tam eşleşme ile kontrol ediliyor
                    match_channel_cleaned = match_channel.strip().lower()
                    m3u_channel_cleaned = channel["name"].strip().lower()

                    # Eşleşen kanalı bulma
                    if match_channel_cleaned == m3u_channel_cleaned and channel["name"] not in written_channels:
                        # Kanal ismini written_channels set'ine ekleyerek tekrar yazılmasını engelliyoruz
                        written_channels.add(channel["name"])

                        # Yeni M3U formatında yaz: "00:00 NAME (CHANNEL)"
                        f.write(f'#EXTINF:-1 tvg-id="None" tvg-name="{channel["name"]}" tvg-logo="{match["logo"]}" '
                                f'group-title="{channel["group_title"]}", {match["time"]} {match["name"]} ({match_channel})\n')
                        f.write('#EXTVLCOPT:http-user-agent=VAVOO/1.0\n')
                        f.write('#EXTVLCOPT:http-referrer=https://vavoo.to/\n')
                        f.write(f'{channel["url"]}\n')
                        f.write("\n")

                        # Eşleşme bulundu, bu maçı işledik
                        match_found = True
                        break
                if match_found:
                    break  # Bu maç için eşleşen kanal bulunduğu için dışarıya çıkıyoruz

            if not match_found:
                print(f"Bu maç işlenmedi: {match['name']} - {match['time']}")  # Hangi maçların işlenmediğini görmek için

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
