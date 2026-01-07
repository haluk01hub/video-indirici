from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# SEO VE GOOGLE UYUMLU ANA SAYFA
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Video İndir - Filigransız Reels & YouTube Kaydet</title>
    <meta name="description" content="TikTok videolarını filigransız indir. Instagram Reels ve YouTube videolarını ücretsiz, HD ve hızlıca kaydedin.">
    <meta name="keywords" content="tiktok video indir, filigransız tiktok, reels indir, instagram video indir, filigransız indir">
    
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #080808; color: white; text-align: center; padding: 10px; }
        .card { max-width: 500px; margin: 20px auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #333; background: #000; color: white; margin-bottom: 20px; outline: none; }
        .btn { width: 95%; padding: 16px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; display: block; margin-left: auto; margin-right: auto; font-size: 16px; transition: 0.3s; }
        .btn-normal { background: #222; color: #888; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #d40000); color: white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
        .h-etiket { color: #ff0000; letter-spacing: -1px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="card">
        <h1 class="h-etiket">Tik-Insta Save</h1>
        <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Ücretsiz Filigransız Video İndirme Aracı</p>
        
        <form id="downloadForm" method="post">
            <input type="text" name="url" placeholder="Video linkini buraya yapıştır..." required>
            <button type="submit" onclick="this.form.action='/hazirla'" class="btn btn-normal">HIZLI İNDİR (SD)</button>
            <button type="submit" onclick="this.form.action='/video_izle'" class="btn btn-premium">✨ FİLİGRANSIZ İNDİR (10s Reklam İzle)</button>
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

# VİDEO İZLEME VE ÖDÜLLÜ REKLAM SAYFASI
VIDEO_WATCH_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hazırlanıyor - Tik-Insta Save</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #000; color: white; text-align: center; padding: 20px; }
        .video-container { max-width: 600px; margin: 20px auto; background: #111; border-radius: 15px; overflow: hidden; position: relative; border: 2px solid #333; }
        .video-placeholder { width: 100%; height: 300px; display: flex; align-items: center; justify-content: center; background: #000; flex-direction: column; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #ff0000; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin-bottom: 15px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #indir-btn { display: none; width: 100%; padding: 20px; background: #28a745; color: white; border: none; font-weight: bold; font-size: 18px; cursor: pointer; }
    </style>
</head>
<body>
    <h3>📽️ Video İşleniyor...</h3>
    <p>Filigransız sürüm için 10 saniye reklamı izleyin.</p>

    <div class="video-container">
        <div style="padding: 10px;">
             <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
             <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
        </div>

        <div class="video-placeholder">
            <div class="spinner"></div>
            <div id="timer" style="font-size: 20px; font-weight: bold;">Video İzleniyor: 10s</div>
        </div>

        <form action="/hazirla" method="post">
            <input type="hidden" name="url" value="{{ url }}">
            <button type="submit" id="indir-btn">📥 FİLİGRANSIZ VİDEOYU İNDİR</button>
        </form>
    </div>
    
    <script>
        let count = 10;
        let timer = document.getElementById('timer');
        let btn = document.getElementById('indir-btn');
        let interval = setInterval(() => {
            count--;
            timer.innerText = "Video İzleniyor: " + count + "s";
            if(count <= 0) {
                clearInterval(interval);
                timer.style.display = 'none';
                document.querySelector('.spinner').style.display = 'none';
                btn.style.display = 'block';
            }
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/video_izle', methods=['POST'])
def video_izle():
    url = request.form.get('url')
    return render_template_string(VIDEO_WATCH_HTML, url=url)

@app.route('/hazirla', methods=['POST'])
def hazirla():
    video_url = request.form.get('url')
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
            ydl.download([video_url])
        return send_file('video.mp4', as_attachment=True)
    except Exception as e:
        return f"Hata: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
