from flask import Flask, request, jsonify
import os
import sys

app = Flask(__name__)

@app.route('/')
def ana_sayfa():
    return "Zeldy API Aktif! /adres?tc=... kullanarak sorgu yapabilirsin."

@app.route('/adres', methods=['GET', 'POST'])
def adres_sorgu():
    tc = request.values.get('tc', '').strip()
    if not tc or len(tc) < 11:
        return jsonify({"Success": False, "Message": "Gecerli TC girin."}), 400

    file_path = 'data.txt'
    if not os.path.exists(file_path):
        return jsonify({"Success": False, "Message": "Veri dosyasi bulunamadi."}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith(tc):
                    parca = line.strip().split(" ")
                    ad_soyad = f"{parca[1]} {parca[2]}" if len(parca) >= 3 else "Belirtilmemiş"
                    return jsonify({
                        "Success": True,
                        "TC": parca[0],
                        "Ad Soyad": ad_soyad,
                        "Data": line.strip(),
                        "Telegram": "https://t.me/Zeldyy_here"
                    })
    except Exception as e:
        return jsonify({"Success": False, "Message": str(e)}), 500

    return jsonify({"Success": False, "Message": "Bulunamadi."}), 404

if _
