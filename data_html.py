import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# ChromeOptions ile tarayıcı seçeneklerini ayarlama
chrome_options = Options()
chrome_options.add_argument('--disable-extensions')  # Uzantıları devre dışı bırak
chrome_options.add_argument('--headless')  # Başlık olmadan çalıştır
chrome_options.add_argument('--no-sandbox')  # Sandboxing'i devre dışı bırak
chrome_options.add_argument('--disable-dev-shm-usage')  # Geliştirici paylaşımlı bellek kullanımını devre dışı bırak

# ChromeDriver'ı yükleyip başlatmak için Service kullanma
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://proxyium.com/')

try:
    # Xpath ile input alanını bul ve 'https://vavoo.to/' adresini yaz
    input_xpath = '/html/body/main/div/div/div[2]/div/div[2]/form/div[2]/input'
    input_field = driver.find_element(By.XPATH, input_xpath)
    input_field.send_keys('https://vavoo.to/')  # URL'yi giriyoruz

    # Xpath ile butonu bul ve tıkla
    button_xpath = '/html/body/main/div/div/div[2]/div/div[2]/form/div[2]/button'
    button = driver.find_element(By.XPATH, button_xpath)
    button.click()

    # 60 saniye bekle (sayfa yüklenene kadar)
    time.sleep(60)

    # Sayfanın HTML içeriğini al
    html_content = driver.page_source

    # HTML'yi data.html dosyasına kaydet
    with open('data.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print('HTML başarıyla kaydedildi.')

except Exception as e:
    print(f"Bir hata oluştu: {e}")

finally:
    # Tarayıcıyı kapat
    driver.quit()
