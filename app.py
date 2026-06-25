from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/adres')
def adres_sorgu():
    tc = request.args.get('tc')
    if not tc:
        return "Lutfen TC girin."

    url = f"https://ornek-api.com/adres.php?tc={tc}"

    try:
        r = requests.get(url, timeout=20)
        veri = r.text

        veri = veri.replace("io7r", "")
        veri = veri.replace("_23", "")
        veri = veri.replace('"', "")
        veri = veri.replace("'", "")
        veri = veri.replace(":", "")
        veri = veri.replace("Id", "")

        return Response(veri.strip(), mimetype='application/json')

    except:
        return Response('{"hata":"Baglanti hatasi"}',
                       mimetype='application/json')

if __name__ == '__main__':
    app.run()
