from flask import Flask, request, jsonify
import re
import os
import hashlib

app = Flask(__name__)

DATA_FILE = 'Newton_Plaka_Data.txt'

@app.route('/plaka', methods=['GET'])
def plaka_sorgu():
    # Parametreleri alıyoruz
    sorgu_plaka = request.args.get('plaka', '').strip().upper()
    sorgu_adi = request.args.get('adi', '').strip()
    sorgu_soyadi = request.args.get('soyadi', '').strip()

    # Eğer hiçbir parametre girilmemişse (PHP'deki hata bloğu)
    if not any([sorgu_plaka, sorgu_adi, sorgu_soyadi]):
        # Mevcut host bilgisini alarak linkleri oluşturuyoruz
        host = request.host_url.rstrip('/')
        return jsonify({
            "hata": "Sorgulama kriteri eksik!",
            "kullanim": {
                "plaka_ile": f"{host}/plaka?plaka=34VY7619",
                "ad_soyad_ile": f"{host}/plaka?adi=Mehmet&soyadi=Yeter"
            },
            "telegram": "https://t.me/Zeldyy_here"
        }), 400

    if not os.path.exists(DATA_FILE):
        return jsonify({"hata": "Veri dosyası bulunamadı."}), 404

    sonuclar = []
    eklenenler = set()
    regex_pattern = r"VALUES\s*\(\d+,\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)'\)"

    with open(DATA_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        for satir in f:
            match = re.search(regex_pattern, satir, re.IGNORECASE)
            if match:
                plaka = match.group(1).strip()
                ad_soyad = match.group(2).strip()
                tarih = match.group(3).strip()
                tel = match.group(4).strip()

                eslesme = False

                # 1. PLAKA SORGUSU
                if sorgu_plaka and plaka.upper() == sorgu_plaka:
                    eslesme = True
                
                # 2. AD SOYAD SORGUSU (Her iki alan da doluysa "VE" mantığıyla çalışır)
                if not eslesme and (sorgu_adi or sorgu_soyadi):
                    ad_ok = True if not sorgu_adi or (sorgu_adi.lower() in ad_soyad.lower()) else False
                    soyad_ok = True if not sorgu_soyadi or (sorgu_soyadi.lower() in ad_soyad.lower()) else False
                    
                    if ad_ok and soyad_ok:
                        eslesme = True

                if eslesme:
                    unique_id = hashlib.md5(f"{plaka}{ad_soyad}{tel}".encode()).hexdigest()
                    if unique_id not in eklenenler:
                        sonuclar.append({
                            "plaka": plaka,
                            "sahibi": ad_soyad,
                            "tarih": tarih,
                            "telefon": tel
                        })
                        eklenenler.add(unique_id)

    return jsonify({
        "durum": "basarili",
        "toplam": len(sonuclar),
        "data": sonuclar,
        "telegram": "https://t.me/Zeldyy_here"
    })

if __name__ == '__main__':
    app.run(debug=True)
  
