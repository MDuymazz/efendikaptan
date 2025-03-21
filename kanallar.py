from bs4 import BeautifulSoup

# Örnek ülke isimleri listesi (bu listeyi daha fazla ülke adı ile genişletebilirsiniz)
country_names = [
    "Albania", "Arabia", "Balkans", "Bulgaria", "France", "Germany", "Italy", 
    "Netherlands", "Poland", "Portugal", "Romania", "Russia", "Spain", "Turkey", 
    "United Kingdom", "Argentina", "Mexico", "Egypt", "Saudi Arabia", "South Africa", "Nigeria"
]

# 'data.html' dosyasından HTML içeriğini oku
with open('data.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup ile HTML içeriğini parse et
soup = BeautifulSoup(html_content, 'html.parser')

# <button> etiketi içinde <span __cpp="1">... </span> olan öğeleri bul
buttons = soup.find_all('button', {'__cpp': '1'})

# Tek bir dosya açıyoruz
with open('all_countries_channels.txt', 'w', encoding='utf-8') as output_file:
    # Her buton için span metnini al ve ona uygun dosya oluştur
    for button in buttons:
        # <span __cpp="1">...</span> içeriğini al
        spans = button.find_all('span', {'__cpp': '1'})
        
        # Her span için işlem yap
        for span in spans:
            span_text = span.text.strip()  # span metnini alıp temizle

            # Eğer metin bir ülke ismi ise
            if span_text in country_names:
                output_file.write(f'Country = "{span_text}"\n')

                # Kanal adı ve buton id bilgilerini al
                channel_div = button.find('div', {'__cpp': '1'})
                
                # Eğer <div __cpp="1"> öğesi varsa, metni al
                if channel_div:
                    channel_name = channel_div.text.strip()

                    # Eğer channel_name içinde ülke adı varsa, o kısmı kaldır
                    for country in country_names:
                        if country in channel_name:
                            channel_name = channel_name.replace(country, "").strip()
                else:
                    channel_name = 'Unknown Channel'

                button_id = button.get('id')
                
                # Button ID'den sadece sayısal kısmı al
                numeric_id = button_id.split('-')[-1]  # 'channel-' kısmını atıyoruz
                
                # Button ID'den URL formatını oluştur
                m3u8_url = f"https://vavoo.to/play/{numeric_id}/index.m3u8"

                # Veriyi dosyaya yaz (önce Channel Name, sonra Button ID URL)
                output_file.write(f'Channel Name: "{channel_name}"\n')
                output_file.write(f'Button ID URL: "{m3u8_url}"\n\n')

print("Tüm veriler 'all_countries_channels.txt' dosyasına başarıyla yazıldı.")
