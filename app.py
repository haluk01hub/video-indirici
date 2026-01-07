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
    <title>TikTok & Instagram Video İndirici - Tik-Insta Save</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #080808; color: white; text-align: center; padding: 10px; }
        .card { max-width: 450px; margin: 30px auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #333; background: #000; color: white; margin-bottom: 20px; outline: none; }
        .btn { width: 100%; padding: 16px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; font-size: 16px; }
        .btn-normal { background: #222; color: #888; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #b30000); color: white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <form action="/islem" method="post">
            <input type="url" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" name="mod" value="normal" class="btn btn-normal">HIZLI İNDİR (SD)</button>
            <button type="submit" name="mod" value="premium" class="btn btn-premium">✨ FİLİGRANSIZ İNDİR (HD + VİDEO)</button>
        </form>
    </div>
    <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
    <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
</body>
</html>
'''

# VİDEO İZLEME VE REKLAM SAYFASI
WAIT_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hazırlanıyor...</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #000; color: white; text-align: center; padding: 20px; }
        .video-box { max-width: 550px; margin: 20px auto; background: #111; border-radius: 15px; border: 1px solid #333; position: relative; overflow: hidden; }
        .fake-player { height: 300px; display: flex; align-items: center; justify-content: center; background: url('https://img.youtube.com/vi/q7X0_tVl9qI/maxresdefault.jpg') center/cover; cursor: pointer; }
        .play-btn { width: 80px; height: 80px; background: rgba(255,0,0,0.8); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; }
        #timer { font-size: 24px; color: #ff0000; margin: 15px 0; font-weight: bold; }
        #indir-btn { display: none; width: 100%; padding: 20px; background: #28a745; color: white; border: none; font-weight: bold; font-size: 18px; cursor: pointer; }
    </style>
</head>
<body>
    <h3>📽️ Filigransız Sürüm Hazırlanıyor</h3>
    <p>Lütfen videoyu başlatın ve 10 saniye bekleyin.</p>

    <div class="video-box">
        <div class="fake-player" onclick="window.open('https://www.effectivegatecpm.com/et6wj2f9?key=62e749d77eb3f45ce41046a596605850', '_blank'); startTimer();">
            <div class="play-btn">▶</div>
        </div>
        
        <div id="timer">Video bekleniyor...</div>

        <form action="/indir_final" method="post">
            <input type="hidden" name="url" value="{{ url }}">
            <button type="submit" id="indir-btn">📥 ŞİMDİ HD İNDİR</button>
        </form>
    </div>

    <script>
        let s = 10;
        let active = false;
        function startTimer() {
            if(active) return;
            active = true;
            let i = setInterval(() => {
                s--;
                document.getElementById('timer').innerText = "Video İşleniyor: " + s + "s";
                if(s <= 0) {
                    clearInterval(i);
                    document.getElementById('timer').style.display='none';
                    document.getElementById('indir-btn').style.display='block';
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
        return indir_islem(url, 'worst') # Hızlı indirme (Normal)

@app.route('/indir_final', methods=['POST'])
def indir_final():
    url = request.form.get('url')
    return indir_islem(url, 'best') # Yüksek kalite (Premium)

def indir_islem(url, kalite):
    ydl_opts = {
        'format': kalite,
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
