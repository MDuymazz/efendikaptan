# M3U dosyasındaki verileri oku (group-title="TURKEY" ve group-title="SPOR YAYINLARI" olanları al)
def read_m3u_file(m3u_file):
    channels = []
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        channel_info = {}
        for line in lines:
            if 'group-title="TURKEY"' in line or 'group-title="SPOR YAYINLARI"' in line:  # İki group-title'ı kontrol et
                # Kanal adı ve diğer bilgileri al
                parts = line.split('tvg-name="')
                if len(parts) > 1:
                    channel_info["name"] = parts[1].split('"')[0]  # Kanal adı (tvg-name içindeki isim)
                
                # URL'nin bulunduğu satır, her zaman 4. satırda (sonuncu satır)
                url = lines[lines.index(line) + 3].strip()  # Stream URL
                channel_info["url"] = url
                channel_info["group_title"] = "GÜNLÜK SPOR AKIŞI"  # group-title her zaman SPOR EKRANI olacak
                channels.append(channel_info)
                channel_info = {}
        return channels


# Veri dosyasındaki maç bilgilerini oku (4'lü grup halinde)
def read_veri_txt(veri_file):
    matches = []
    match_info = {}
    with open(veri_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):  # 4'er 4'er oku
            try:
                match_info["name"] = lines[i].split("=")[1].strip()  # MAÇ ADI
                match_info["time"] = lines[i+1].split("=")[1].strip()  # SAAT
                match_info["channels"] = [lines[i+2].split("=")[1].strip()]  # KANAL
                match_info["logo"] = lines[i+3].split("=")[1].strip()  # LOGO URL
                matches.append(match_info)
                match_info = {}  # Yeni maç için sıfırla
            except IndexError:
                continue  # Eğer 4 satırdan eksik veri varsa, geç
    return matches


# Yeni M3U dosyasını oluştur
def create_new_m3u(m3u_channels, match_details, output_file):
    match_details_sorted = sorted(match_details, key=lambda x: x["time"])  # Saat bilgisine göre sıralama

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")  # Dosyanın en başına #EXTM3U ekleniyor
        
        # Kanal başına yalnızca bir kez yazma
        written_channels = set()

        for match in match_details_sorted:
            match_found = False  # Bu maç için eşleşen kanal bulup bulmadığımızı takip etmek için
            for channel in m3u_channels:
                for match_channel in match["channels"]:  # Bir maç birden fazla kanala sahip olabilir
                    # Kanal adı temizleme: Boşlukları baştan ve sondan temizle
                    match_channel_cleaned = match_channel.strip()  # .strip() kullanarak boşlukları temizle
                    m3u_channel_cleaned = channel["name"].strip()  # M3U kanal adındaki boşlukları temizle

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
