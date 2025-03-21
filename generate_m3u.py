import re

# Dosyayı okuma ve verileri işleme
input_file = "all_countries_channels.txt"  # Verilerin bulunduğu txt dosyasının adı
output_file = "vavoo.m3u"  # Çıktı dosyasının adı

# Çıktı dosyasını açıyoruz
with open(output_file, "w", encoding="utf-8") as output:
    # txt dosyasını okuyoruz
    with open(input_file, "r", encoding="utf-8") as file:
        country = None
        channel_name = None
        button_id_url = None
        first_entry = True  # İlk kanal için #EXTM3U yazılacak, sonrakilerde yazılmayacak
        
        for line in file:
            # Satırdaki 'Country', 'Channel Name' ve 'Button ID URL' bilgilerini kontrol ediyoruz
            if line.startswith("Country = "):
                country = line.split('=')[1].strip().strip('"')  # Ülke ismini al
            elif line.startswith("Channel Name: "):
                channel_name = line.replace("Channel Name: ", "").strip().strip('"')  # Kanal ismini al
            elif line.startswith("Button ID URL: "):
                button_id_url = line.split(':', 1)[1].strip().strip('"')  # Buton ID URL'sini al

                # Tüm veriler toplandıysa, M3U formatında yazalım
                if country and channel_name and button_id_url:
                    if first_entry:
                        output.write("#EXTM3U\n\n\n")  # İlk kanal için #EXTM3U ekliyoruz
                        first_entry = False  # İlk kanal yazıldı, bundan sonra eklenmeyecek

                    # Fazladan çift tırnakları temizle
                    clean_channel_name = channel_name.replace('"', '')

                    m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="" group-title="{country.upper()}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{button_id_url}\n
"""
                    # İçeriği output dosyasına yazıyoruz
                    output.write(m3u_content)
                    
                    # Veriyi sıfırlıyoruz, bir sonraki kanal için
                    country = channel_name = button_id_url = None

print(f"{output_file} dosyası başarıyla oluşturuldu.")
