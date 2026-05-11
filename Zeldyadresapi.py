from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Ana sayfa (Tarayıcıya direkt girdiğinde çalışır)
@app.route('/')
def ana_sayfa():
    return "<h1>Zeldy API Aktif!</h1> Sorgu için: /adres?tc=11HANELITC"

# Adres sorgu ucu
@app.route('/adres', methods=['GET', 'POST'])
def adres_sorgu():
    # PHP'deki $_REQUEST mantığı
    tc = request.values.get('tc', '').strip()
    
    if not tc or len(tc) < 11:
        return jsonify({"Success": False, "Message": "Gecerli TC girin."}), 400

    file_path = 'data.txt'
    if not os.path.exists(file_path):
        return jsonify({"Success": False, "Message": "Veri dosyasi (data.txt) bulunamadi."}), 404

    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(tc):
                        parca = line.split(" ")
                        # En az 3 parça varsa (TC, Ad, Soyad)
                        ad_soyad = f"{parca[1]} {parca[2]}" if len(parca) >= 3 else "Belirtilmemiş"
                        
                        return jsonify({
                            "Success": True,
                            "TC": parca[0],
                            "Ad Soyad": ad_soyad,
                            "Data": line,
                            "Telegram": "https://t.me/Zeldyy_here"
                        })
    except Exception as e:
        return jsonify({"Success": False, "Message": f"Sunucu hatası: {str(e)}"}), 500

    return jsonify({"Success": False, "Message": "Bulunamadi."}), 404


