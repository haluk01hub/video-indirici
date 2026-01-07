from flask import Flask, render_template_string, request, redirect
import yt_dlp
import time

app = Flask(__name__)

# ANA SAYFA TASARIMI
ANA_SAYFA_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ProDownloader - Video İndir</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f0f0f; color: white; text-align: center; padding: 50px; }
        .box { background: #1e1e1e; padding: 30px; border-radius: 20px; display: inline-block; width: 100%; max-width: 450px; border: 1px solid #333; }
        input { width: 90%; padding: 15px; margin-bottom: 20px; border-radius: 10px; border: none; background: #2b2b2b; color: white; }
        .btn { background: #ff4757; color: white; padding: 15px 30px; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; width: 95%; }
    </style>
</head>
<body>
    <div class="box">
        <h1>ProDownloader</h1>
        <form action="/hazirla" method="post">
            <input type="text" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" class="btn">4K İndir (Reklam İzle)</button>
        </form>
    </div>
</body>
</html>
"""

# BEKLEME VE REKLAM SAYFASI TASARIMI
BEKLEME_SAYFASI_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Lütfen Bekleyin...</title>
    <style>
        body { font-family: sans-serif; background: #0f0f0f; color: white; text-align: center; padding: 50px; }
        .ad-area { width: 300px; height: 250px; background: #333; margin: 20px auto; display: flex; align-items: center; justify-content: center; border: 1px dashed #777; }
        #countdown { font-size: 40px; color: #ff4757; font-weight: bold; }
        .download-btn { display: none; background: #2ed573; color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Videonuz Hazırlanıyor...</h2>
    <div class="ad-area">BURAYA REKLAM GELECEK</div>
    
    <p>Lütfen <span id="countdown">10</span> saniye bekleyin.</p>
    
    <div class="ad-area">BURAYA REKLAM GELECEK</div>

    <a href="{{ video_link }}" id="downloadBtn" class="download-btn">VİDEOYU ŞİMDİ İNDİR</a>

    <script>
        var seconds = 10;
        var countdown = document.getElementById('countdown');
        var btn = document.getElementById('downloadBtn');

        var timer = setInterval(function() {
            seconds--;
            countdown.innerText = seconds;
            if (seconds <= 0) {
                clearInterval(timer);
                countdown.parentElement.style.display = 'none';
                btn.style.display = 'inline-block';
            }
        }, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(ANA_SAYFA_HTML)

@app.route('/hazirla', methods=['POST'])
def hazirla():
    url = request.form.get('url')
    try:
        # En iyi hazır birleşik formatı (best) çekiyoruz
        ydl_opts = ydl_opts = ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Daha esnek format seçimi
    'cookiefile': 'cookies.txt',
    'quiet': True,
    'no_warnings': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            link = info.get('url')
        return render_template_string(BEKLEME_SAYFASI_HTML, video_link=link)
    except Exception as e:
        return f"Hata: {e}"

if __name__ == '__main__':

    app.run(debug=True)

