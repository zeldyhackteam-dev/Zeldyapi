from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Merhaba, API çalışıyor!'

# ÖNEMLİ: Eğer başka rotaların varsa onları da buraya ekle
