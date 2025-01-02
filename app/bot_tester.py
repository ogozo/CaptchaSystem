import requests
import random
import string

# Server URL (Gerekirse ayarlayın)
BASE_URL = "http://127.0.0.1:8000/captcha"

# Rastgele giriş üreten fonksiyon (Büyük harfler ve rakamlar karışık)
def random_string():
    characters = string.ascii_uppercase + string.digits  # Büyük harfler ve rakamlar
    return ''.join(random.choices(characters, k=6))  # 6 karakter üret

# CAPTCHA testi için fonksiyon
def test_captcha(attempts):
    success_count = 0  # Başarılı giriş sayısı
    fail_count = 0     # Başarısız giriş sayısı

    for i in range(attempts):
        try:
            # 1. CAPTCHA al
            response = requests.get(f"{BASE_URL}/generate-captcha")
            if response.status_code != 200:
                print(f"Error fetching CAPTCHA: {response.status_code}")
                continue

            data = response.json()
            token = data['token']
            captcha_image = data['captcha_image']

            # 2. Rastgele giriş oluştur
            user_input = random_string()
            print(f"Attempt {i+1}: Trying input '{user_input}'")

            # 3. CAPTCHA doğrula
            verify_response = requests.post(
                f"{BASE_URL}/verify-captcha",
                json={"token": token, "user_input": user_input}
            )

            # 4. Sonucu kontrol et
            result = verify_response.json()
            if result.get("success"):
                print(f"Success for input '{user_input}'!")
                success_count += 1
            else:
                print(f"Failed for input '{user_input}'.")
                fail_count += 1

        except Exception as e:
            print(f"Error: {e}")
            fail_count += 1

    # Sonuçları ekrana yaz
    print("\n--- CAPTCHA Test Results ---")
    print(f"Total Attempts: {attempts}")
    print(f"Successful Attempts: {success_count}")
    print(f"Failed Attempts: {fail_count}")

# Kaç deneme yapılacak?
test_captcha(100)
