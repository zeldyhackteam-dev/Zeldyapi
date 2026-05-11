from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Veri dosyasının ismi (data.txt veya adres.txt olarak değiştirebilirsin)
FILE_PATH = 'data.txt'

@app.route('/adres', methods=['GET', 'POST'])
def adres_sorgu():
    # PHP'deki $_REQUEST['tc'] karşılığı
    tc = request.values.get('tc', '').strip()

    # Giriş kontrolü (11 haneli TC kontrolü)
    if not tc or len(tc) < 11:
        return jsonify({
            "Success": False, 
            "Message": "Gecerli TC girin."
        }), 400

    # Dosya varlık kontrolü
    if not os.path.exists(FILE_PATH):
        return jsonify({
            "Success": False, 
            "Message": "Veri dosyasi bulunamadi."
        }), 404

    found_data = None

    # Dosyayı satır satır tarama
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Satır TC ile başlıyorsa veriyi al
                if line.startswith(tc):
                    found_data = line
                    break
    except Exception as e:
        return jsonify({"Success": False, "Message": f"Sunucu hatası: {str(e)}"}), 500

    if found_data:
        # Veriyi parçalara ayırma
        parca = found_data.split(" ")
        
        # PHP'deki mantıkla Ad ve Soyad birleştirme
        ad_soyad = "Belirtilmemiş"
        if len(parca) >= 3:
            ad_soyad = f"{parca[1]} {parca[2]}"

        # JSON Yanıtı
        return jsonify({
            "Success": True,
            "TC": parca[0],
            "Ad Soyad": ad_soyad,
            "Data": found_data,
            "Telegram": "https://t.me/Zeldyy_here"
        })
    else:
        return jsonify({
            "Success": False, 
            "Message": "Bulunamadi."
        }), 404


    

