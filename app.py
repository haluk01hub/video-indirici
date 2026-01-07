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
        .btn { width: 100%; padding: 16px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; font-size: 16px; }
        .btn-normal { background: #222; color: #aaa; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #b30000); color: white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <form action="/islem" method="post">
            <input type="url" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" name="mod" value="normal" class="btn btn-normal">STANDART İNDİR (Düşük Boyut)</button>
            <button type="submit" name="mod" value="premium" class="btn btn-premium">✨ HD FİLİGRANSIZ (10s Reklam)</button>
        </form>
    </div>
    
    <div id="ad-space" style="margin-top:20px; min-height:100px;">
        <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
        <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
    </div>
</body>
</html>
'''

# BEKLEME VE VİDEO REKLAM SAYFASI
WAIT_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HD Hazırlanıyor...</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #000; color: white; text-align: center; padding: 20px; }
        .loader-box { max-width: 500px; margin: 50px auto; background: #111; padding: 30px; border-radius: 20px; border: 2px solid #ff0000; }
        #timer { font-size: 40px; color: #ff0000; font-weight: bold; margin: 20px 0; }
        #indir-link { display: none; padding: 15px 30px; background: #28a745; color: white; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 18px; }
    </style>
</head>
<body>
    <div class="loader-box">
        <h3>HD Video Filigransız Hazırlanıyor</h3>
        <p>Lütfen bekleyin, video bittiğinde buton açılacak.</p>
        <div id="timer">10</div>

        <div style="margin: 20px 0; background: #1a1a1a; padding: 10px; border-radius: 10px;">
             <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
             <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
        </div>

        <form action="/indir_final" method="post">
            <input type="hidden" name="url" value="{{ url }}">
            <input type="hidden" name="kalite" value="high">
            <button type="submit" id="indir-link" style="border:none; width:100%;">📥 HD VİDEOYU ŞİMDİ İNDİR</button>
        </form>
    </div>

    <script>
        let s = 10;
        let t = document.getElementById('timer');
        let b = document.getElementById('indir-link');
        let i = setInterval(() => {
            s--; t.innerText = s;
            if(s <= 0) { clearInterval(i); t.style.display='none'; b.style.display='block'; }
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def ana_sayfa():
    return render_template_string(INDEX_HTML)

@app.route('/islem', methods=['POST'])
def islem():
    url = request.form.get('url')
    mod = request.form.get('mod')
    if mod == 'premium':
        return render_template_string(WAIT_HTML, url=url)
    else:
        return indir_çek(url, 'low')

@app.route('/indir_final', methods=['POST'])
def indir_final():
    url = request.form.get('url')
    return indir_çek(url, 'high')

def indir_çek(url, kalite):
    # KALİTE FARKI BURADA YAPILIYOR
    if kalite == 'high':
        # En iyi video ve en iyi sesi bulup birleştirir (HD)
        ydl_format = 'bestvideo+bestaudio/best'
    else:
        # Hızlı indirme için orta kalite mp4 seçer
        ydl_format = 'best[ext=mp4]/worst'

    ydl_opts = {
        'format': ydl_format,
        'outtmpl': 'video.mp4',
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        if os.path.exists('video.mp4'): os.remove('video.mp4')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file('video.mp4', as_attachment=True)
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
