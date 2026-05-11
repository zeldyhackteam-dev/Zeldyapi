from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ANA SAYFA - Render'ın 'bu uygulama yaşıyor' demesi için şart!
@app.route('/')
def home():
    return "Zeldy API Aktif!"

# SORGUNUN YAPILDIĞI YER
@app.route('/adres', methods=['GET', 'POST'])
def adres_sorgu():
    tc = request.values.get('tc', '').strip()
    
    if not tc or len(tc) < 11:
        return jsonify({"Success": False, "Message": "Gecerli TC girin."}), 400

    file_path = 'data.txt'
    if not os.path.exists(file_path):
        return jsonify({"Success": False, "Message": "data.txt dosyasi bulunamadi."}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith(tc):
                    parca = line.split(" ")
                    ad_soyad = f"{parca[1]} {parca[2]}" if len(parca) >= 3 else "Belirtilmemiş"
                    return jsonify({
                        "Success": True,
                        "TC": parca[0],
                        "Ad Soyad": ad_soyad,
                        "Data": line,
                        "Telegram": "https://t.me/Zeldyy_here"
                    })
    except Exception as e:
        return jsonify({"Success": False, "Message": str(e)}), 500

    return jsonify({"Success": False, "Message": "Bulunamadi."}), 404

if __name__ == '__main__':
    # Render'ın istediği port ayarı tam olarak budur!
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
                  
