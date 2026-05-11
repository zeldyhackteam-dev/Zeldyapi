from flask import Flask, request, jsonify
import os
import logging

# Logları Render panelinde görebilmek için ayar
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Zeldy API Aktif!</h1> Sorgu için /adres?tc=... kullanın."

@app.route('/adres', methods=['GET', 'POST'])
def adres_sorgu():
    tc = request.values.get('tc', '').strip()
    
    if not tc or len(tc) < 11:
        return jsonify({"Success": False, "Message": "Gecerli TC girin."}), 400

    file_path = 'data.txt'
    if not os.path.exists(file_path):
        logging.error("HATA: data.txt dosyasi bulunamadi!")
        return jsonify({"Success": False, "Message": "Veri dosyasi bulunamadi."}), 404

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
        logging.error(f"Sorgu hatasi: {str(e)}")
        return jsonify({"Success": False, "Message": str(e)}), 500

    return jsonify({"Success": False, "Message": "Bulunamadi."}), 404

if __name__ == '__main__':
    # Render'ın portu görmesi için burası çok kritik
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
  
