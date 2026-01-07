from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# ANA SAYFA TASARIMI
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Video İndir - Tik-Insta Save</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #080808; color: white; text-align: center; padding: 10px; }
        .card { max-width: 500px; margin: 20px auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #333; background: #000; color: white; margin-bottom: 20px; outline: none; }
        .btn { width: 95%; padding: 16px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; display: block; margin: 10px auto; font-size: 16px; transition: 0.3s; text-decoration: none; }
        .btn-normal { background: #222; color: #888; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #d40000); color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" formaction="/indir_normal" class="btn btn-normal">HIZLI İNDİR (Standart)</button>
            <button type="submit" formaction="/video_izle" class="btn btn-premium">✨ FİLİGRANSIZ İNDİR (HD + İZLE)</button>
        </form>
    </div>
    <script src="https://pl28425051.effectivegatecpm.com/05/7c/5d/057c5d1e6ff12fbdc9c2341da887dd7c.js"></script>
</body>
</html>
'''

# VİDEO İZLEME SAYFASI
VIDEO_WATCH_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hazırlanıyor...</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #000; color: white; text-align: center; padding: 20px; }
        .video-box { max-width: 500px; margin: 20px auto; background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; }
        #timer { font-size: 24px; color: #ff0000; font-weight: bold; margin: 20px 0; }
        #indir-btn { display: none; width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="video-box">
        <h3>Filigransız HD Video Hazırlanıyor</h3>
        <div id="timer">10s</div>
        
        <div style="margin: 20px 0;">
             <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
             <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
        </div>

        <form action="/indir_premium" method="post">
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

def download_video(url, is_premium=False):
    # Premium seçilirse en iyi kaliteyi, normalde ise standart kaliteyi zorla
    fmt = 'bestvideo+bestaudio/best' if is_premium else 'best[ext=mp4]/best'
    
    ydl_opts = {
        'format': fmt,
        'outtmpl': 'video.mp4',
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    if os.path.exists('video.mp4'): os.remove('video.mp4')
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'video.mp4'

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/video_izle', methods=['POST'])
def video_izle():
    url = request.form.get('url')
    return render_template_string(VIDEO_WATCH_HTML, url=url)

@app.route('/indir_normal', methods=['POST'])
def indir_normal():
    url = request.form.get('url')
    path = download_video(url, is_premium=False)
    return send_file(path, as_attachment=True)

@app.route('/indir_premium', methods=['POST'])
def indir_premium():
    url = request.form.get('url')
    path = download_video(url, is_premium=True)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
