from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# ANA SAYFA - Tasarım ve Reklamlar
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tik-Insta Save - Video İndirici</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #080808; color: white; text-align: center; padding: 10px; }
        .card { max-width: 500px; margin: 20px auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #333; background: #000; color: white; margin-bottom: 20px; outline: none; }
        .btn { width: 95%; padding: 16px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; display: block; margin: 10px auto; font-size: 16px; transition: 0.3s; }
        .btn-normal { background: #222; color: #888; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #d40000); color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <form action="/yonlendir" method="post">
            <input type="text" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" name="tip" value="normal" class="btn btn-normal">HIZLI İNDİR (Standart)</button>
            <button type="submit" name="tip" value="premium" class="btn btn-premium">✨ FİLİGRANSIZ İNDİR (HD + İZLE)</button>
        </form>
    </div>
    
    <div style="margin-top:20px;">
        <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
        <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
    </div>

    <script src="https://pl28425051.effectivegatecpm.com/05/7c/5d/057c5d1e6ff12fbdc9c2341da887dd7c.js"></script>
</body>
</html>
'''

# VİDEO İZLEME / SAYAÇ SAYFASI
WAITING_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hazırlanıyor...</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #000; color: white; text-align: center; padding: 20px; }
        .box { max-width: 500px; margin: 40px auto; background: #111; padding: 30px; border-radius: 15px; border: 1px solid #333; }
        #timer { font-size: 30px; color: #ff0000; font-weight: bold; margin: 20px 0; }
        #indir-btn { display: none; width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h3>HD Video İşleniyor...</h3>
        <p>Videonuz hazırlanırken lütfen bekleyin.</p>
        <div id="timer">10s</div>

        <div style="min-height: 200px; margin: 20px 0;">
             <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
             <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
        </div>

        <form action="/indir" method="post">
            <input type="hidden" name="url" value="{{ url }}">
            <button type="submit" id="indir-btn">📥 ŞİMDİ HD İNDİR</button>
        </form>
    </div>

    <script>
        let count = 10;
        let t = document.getElementById('timer');
        let b = document.getElementById('indir-btn');
        let interval = setInterval(() => {
            count--;
            t.innerText = count + "s";
            if(count <= 0) {
                clearInterval(interval);
                t.style.display = 'none';
                b.style.display = 'block';
            }
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/yonlendir', methods=['POST'])
def yonlendir():
    url = request.form.get('url')
    tip = request.form.get('tip')
    if tip == 'premium':
        return render_template_string(WAITING_HTML, url=url)
    else:
        # Normal indirme için doğrudan indirme fonksiyonuna git
        return indir_islem(url)

@app.route('/indir', methods=['POST'])
def indir_sayfa():
    url = request.form.get('url')
    return indir_islem(url)

def indir_islem(url):
    ydl_opts = {
        'format': 'best',
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
        return f"Hata: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
