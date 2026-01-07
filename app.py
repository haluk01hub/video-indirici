from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# ANA SAYFA
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Tik-Insta Save - HD Video İndir</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #080808; color: white; text-align: center; padding: 10px; margin: 0; }
        .card { max-width: 400px; margin: 40px auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; }
        input { width: 100%; box-sizing: border-box; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #000; color: white; margin-bottom: 20px; font-size: 16px; outline: none; }
        .btn { width: 100%; padding: 18px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; font-size: 16px; transition: 0.3s; }
        .btn-normal { background: #222; color: #888; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #b30000); color: white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
        h1 { font-size: 24px; letter-spacing: -1px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <p style="color:#666; font-size:14px; margin-bottom:20px;">Filigransız Mobil & PC Uyumlu</p>
        <form action="/islem" method="post">
            <input type="url" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" name="mod" value="normal" class="btn btn-normal">STANDART İNDİR (SD)</button>
            <button type="submit" name="mod" value="premium" class="btn btn-premium">✨ HD FİLİGRANSIZ (10s İZLE)</button>
        </form>
    </div>
    
    <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
    <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
</body>
</html>
'''

# MOBİL UYUMLU REKLAM VE SAYAÇ SAYFASI
WAIT_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HD Hazırlanıyor...</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #000; color: white; text-align: center; padding: 30px; }
        .box { max-width: 400px; margin: 0 auto; background: #111; padding: 30px; border-radius: 20px; border: 1px solid #ff0000; }
        #timer { font-size: 50px; color: #ff0000; font-weight: bold; margin: 20px 0; }
        .info-text { color: #aaa; margin-bottom: 20px; font-size: 15px; }
        .btn-action { width: 100%; padding: 20px; border: none; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; text-decoration: none; display: block; }
        #indir-btn { display: none; background: #28a745; color: white; }
        .ad-button { background: #fff; color: #000; }
        .btn-home { background: #333; color: #fff; font-size: 14px; padding: 12px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="box">
        <h3>📽️ Video Hazırlanıyor</h3>
        <p class="info-text">İşlemi başlatmak için aşağıdaki butona basın ve 10 saniye bekleyin.</p>
        
        <a href="https://www.effectivegatecpm.com/et6wj2f9?key=62e749d77eb3f45ce41046a596605850" 
           target="_blank" 
           class="btn-action ad-button" 
           onclick="startTimer()">
           VİDEOYU İZLE VE İNDİR
        </a>

        <div id="timer" style="display:none;">10</div>

        <form action="/indir_final" method="post" id="downloadForm">
            <input type="hidden" name="url" value="{{ url }}">
            <button type="submit" id="indir-btn" class="btn-action" onclick="showHomeBtn()">📥 HD FİLİGRANSIZ İNDİR</button>
        </form>

        <a href="/" id="home-btn" class="btn-action btn-home" style="display:none;">🏠 Başka Video İndir</a>
    </div>

    <script>
        let s = 10;
        function startTimer() {
            document.querySelector('.ad-button').style.display = 'none';
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

        function showHomeBtn() {
            // Kullanıcı indir butonuna bastığında "Başka Video İndir" butonu görünür hale gelsin
            setTimeout(() => {
                document.getElementById('home-btn').style.display = 'block';
            }, 2000);
        }
    </script>
</body>
</html>
'''

# --- İndirme Fonksiyonları ---
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
    ydl_opts = {'format': kalite, 'outtmpl': 'video.mp4', 'cookiefile': 'cookies.txt', 'quiet': True, 'nocheckcertificate': True, 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    try:
        if os.path.exists('video.mp4'): os.remove('video.mp4')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        return send_file('video.mp4', as_attachment=True)
    except Exception as e: return f"Hata: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
