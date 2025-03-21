from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Chrome seçeneklerini ayarlıyoruz
chrome_options = Options()
chrome_options.add_argument("--headless")  # Başsız modda çalıştırma (isteğe bağlı)
chrome_options.add_argument("--no-sandbox")  # Bazı sistemlerde sandbox modunun kapatılması gerekebilir
chrome_options.add_argument("--disable-dev-shm-usage")  # Dev/shm kullanımını devre dışı bırakma
chrome_options.add_argument(f"user-data-dir=/tmp/chrome-user-data-dir")  # Geçici bir user data dizini kullanıyoruz

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

    # 30 saniye bekle
    time.sleep(30)

    # Sayfanın HTML içeriğini al
    html_content = driver.page_source

    # HTML'yi data.html dosyasına kaydet
    with open('data.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print('HTML başarıyla kaydedildi.')

finally:
    # Tarayıcıyı kapat
    driver.quit()
