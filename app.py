from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# ANA SAYFA - Tasarım Kaymaları Fixlendi
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tik-Insta Save - HD Video İndir</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #080808; color: white; text-align: center; margin: 0; padding: 20px; }
        .card { max-width: 400px; margin: 0 auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; display: flex; flex-direction: column; align-items: center; }
        h1 { font-size: 26px; margin-bottom: 5px; color: #fff; }
        .sub-text { color: #666; font-size: 14px; margin-bottom: 25px; }
        form { width: 100%; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #000; color: white; margin-bottom: 15px; font-size: 16px; outline: none; }
        .btn { width: 100%; padding: 18px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; font-size: 16px; margin-bottom: 10px; transition: 0.2s; }
        .btn-normal { background: #222; color: #aaa; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #b30000); color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <div class="sub-text">Mobil & PC Uyumlu Video İndirici</div>
        <form action="/islem" method="post">
            <input type="url" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" name="mod" value="normal" class="btn btn-normal">HIZLI İNDİR (SD)</button>
            <button type="submit" name="mod" value="premium" class="btn btn-premium">✨ HD FİLİGRANSIZ (10s İZLE)</button>
        </form>
    </div>
    <div style="margin-top:20px;">
        <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
        <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
    </div>
</body>
</html>
'''

# BEKLEME SAYFASI - Mobil Buton Kayması Fixlendi
WAIT_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>HD Hazırlanıyor...</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #000; color: white; text-align: center; margin: 0; padding: 20px; }
        .box { max-width: 400px; margin: 20px auto; background: #111; padding: 30px; border-radius: 20px; border: 1px solid #ff0000; display: flex; flex-direction: column; align-items: center; }
        #timer { font-size: 60px; color: #ff0000; font-weight: bold; margin: 20px 0; }
        .btn-main { width: 100%; padding: 20px; border: none; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; text-decoration: none; display: block; }
        .ad-btn { background: #fff; color: #000; }
        #indir-btn { display: none; background: #28a745; color: white; margin-bottom: 15px; }
        .btn-home { background: #333; color: #fff; font-size: 14px; padding: 15px; display: none; }
    </style>
</head>
<body>
    <div class="box">
        <h3>📽️ Video İşleniyor</h3>
        <p style="color:#aaa; font-size:14px;">Reklamı izleyin, indirme butonu açılacaktır.</p>
        
        <a href="https://www.effectivegatecpm.com/et6wj2f9?key=62e749d77eb3f45ce41046a596605850" 
           target="_blank" 
           id="ad-link"
           class="btn-main ad-btn" 
           onclick="startTimer()">
           VİDEOYU İZLE
        </a>

        <div id="timer" style="display:none;">10</div>

        <form action="/indir_final" method="post" id="dlForm" style="width:100%;">
            <input type="hidden" name="url" value="{{ url }}">
            <button type="submit" id="indir-btn" class="btn-main" onclick="showHome()">📥 HD VİDEOYU İNDİR</button>
        </form>

        <a href="/" id="home-link" class="btn-main btn-home">🏠 Başka Video İndir</a>
    </div>

    <script>
        let s = 10;
        function startTimer() {
            document.getElementById('ad-link').style.display = 'none';
            document.getElementById('timer').style.display = 'block';
            let i = setInterval(() => {
                s--;
                document.getElementById('timer').innerText = s;
                if(s <= 0) {
                    clearInterval(i);
                    document.getElementById('timer').style.display = 'none';
                    document.getElementById('indir-btn').style.display = 'block';
                }
            }, 1000);
        }
        function showHome() {
            setTimeout(() => {
                document.getElementById('home-link').style.display = 'block';
            }, 2000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(INDEX_HTML)

@app.route('/islem', methods=['POST'])
def islem():
    url = request.form.get('url'); mod = request.form.get('mod')
    if mod == 'premium': return render_template_string(WAIT_HTML, url=url)
    else: return indir_islem(url, 'worst')

@app.route('/indir_final', methods=['POST'])
def indir_final():
    url = request.form.get('url'); return indir_islem(url, 'best')

def indir_islem(url, kalite):
    ydl_opts = {'format': kalite, 'outtmpl': 'video.mp4', 'cookiefile': 'cookies.txt', 'quiet': True, 'nocheckcertificate': True, 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'}
    try:
        if os.path.exists('video.mp4'): os.remove('video.mp4')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        return send_file('video.mp4', as_attachment=True)
    except Exception as e: return f"Hata: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
