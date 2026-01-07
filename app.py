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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tik-Insta Save - Hızlı Video İndir</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #080808; color: white; text-align: center; padding: 10px; }
        .card { max-width: 450px; margin: 30px auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #333; background: #000; color: white; margin-bottom: 20px; outline: none; }
        .btn { width: 100%; padding: 16px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; font-size: 16px; transition: 0.3s; }
        .btn-normal { background: #222; color: #888; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #b30000); color: white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
        .btn-premium:hover { transform: scale(1.02); }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <p style="color:#666; font-size:14px;">Filigransız HD Video İndirme Aracı</p>
        <form action="/islem" method="post">
            <input type="url" name="url" placeholder="Video linkini buraya yapıştır..." required>
            <button type="submit" name="mod" value="normal" class="btn btn-normal">HIZLI İNDİR (Standart)</button>
            <button type="submit" name="mod" value="premium" class="btn btn-premium">✨ HD FİLİGRANSIZ (POP-UP REKLAM)</button>
        </form>
    </div>
    
    <div style="margin-top:20px;">
        <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
        <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
    </div>
</body>
</html>
'''

# REKLAMLI BEKLEME SAYFASI (Pop-up Aynı Sekmede)
WAIT_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hazırlanıyor...</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #000; color: white; text-align: center; margin: 0; padding: 0; overflow: hidden; }
        
        /* POP-UP REKLAM ALANI */
        #ad-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #fff; z-index: 9999; display: block;
        }
        .close-bar {
            position: absolute; top: 0; left: 0; width: 100%; height: 50px;
            background: #ff0000; color: white; display: flex; align-items: center;
            justify-content: center; font-weight: bold; cursor: pointer; z-index: 10001;
        }
        iframe { width: 100%; height: calc(100% - 50px); border: none; margin-top: 50px; }

        .loader-content { padding: 50px 20px; }
        #timer { font-size: 60px; color: #ff0000; font-weight: bold; margin: 20px 0; }
        #indir-btn { display: none; padding: 20px 40px; background: #28a745; color: white; border: none; border-radius: 12px; font-size: 20px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>

    <div id="ad-overlay">
        <div class="close-bar" id="close-btn" onclick="closeAd()">REKLAMI GEÇ VE İNDİR [X]</div>
        <iframe src="https://www.effectivegatecpm.com/et6wj2f9?key=62e749d77eb3f45ce41046a596605850"></iframe>
    </div>

    <div class="loader-content">
        <h2>📽️ Videonuz Hazırlanıyor</h2>
        <p>Lütfen reklamı kapatın, indirme bağlantısı 10 saniye içinde açılacaktır.</p>
        <div id="timer">10</div>

        <form action="/indir_final" method="post">
            <input type="hidden" name="url" value="{{ url }}">
            <button type="submit" id="indir-btn">📥 HD FİLİGRANSIZ İNDİR</button>
        </form>
    </div>

    <script>
        let s = 10;
        let timerDiv = document.getElementById('timer');
        let btn = document.getElementById('indir-btn');
        let ad = document.getElementById('ad-overlay');

        function closeAd() {
            ad.style.display = 'none';
            document.body.style.overflow = 'auto';
            
            // Sayaç reklam kapandıktan sonra başlar
            let interval = setInterval(() => {
                s--;
                timerDiv.innerText = s;
                if(s <= 0) {
                    clearInterval(interval);
                    timerDiv.style.display = 'none';
                    btn.style.display = 'inline-block';
                }
            }, 1000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/islem', methods=['POST'])
def islem():
    url = request.form.get('url')
    mod = request.form.get('mod')
    if mod == 'premium':
        return render_template_string(WAIT_HTML, url=url)
    else:
        return indir_islem(url, 'worst') # Standart indirme

@app.route('/indir_final', methods=['POST'])
def indir_final():
    url = request.form.get('url')
    return indir_islem(url, 'best') # HD indirme

def indir_islem(url, kalite):
    ydl_opts = {
        'format': kalite,
        'outtmpl': 'video.mp4',
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    try:
        if os.path.exists('video.mp4'): os.remove('video.mp4')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file('video.mp4', as_attachment=True)
    except Exception as e:
        return f"Hata: Video indirilemedi. Lütfen linki kontrol edin veya daha sonra tekrar deneyin. Detay: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
