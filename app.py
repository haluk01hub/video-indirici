from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Reklam Yerleşimli ve Mobil Uyumlu Tasarım
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hızlı Video İndirici</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0f0f0f; color: #ffffff; text-align: center; padding: 20px; }
        .card { max-width: 500px; margin: 40px auto; background: #1a1a1a; padding: 30px; border-radius: 20px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #000; color: white; margin-bottom: 20px; font-size: 16px; }
        button { width: 95%; padding: 15px; background: linear-gradient(45deg, #ff0000, #ff4444); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 16px; transition: 0.3s; }
        button:hover { transform: scale(1.02); opacity: 0.9; }
        .footer { margin-top: 50px; color: #555; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Video İndirici</h2>
        <p style="color: #aaa;">YouTube, Instagram ve TikTok videolarını anında indir!</p>

        <form action="/hazirla" method="post">
            <input type="text" name="url" placeholder="Video linkini buraya yapıştır..." required>
            <button type="submit">İNDİRMEYİ BAŞLAT</button>
        </form>
    </div>

    <div class="footer">
        © 2026 Video İndirme Hizmeti
    </div>

    <script src="https://pl28425051.effectivegatecpm.com/05/7c/5d/057c5d1e6ff12fbdc9c2341da887dd7c.js"></script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/hazirla', methods=['post'])
def hazirla():
    video_url = request.form.get('url')
    # YouTube bot ve format engellerini aşmak için gelişmiş ayarlar
   ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'no_warnings': True,
        # Rastgele bir istemci gibi görünmek için başlıkları zorla
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }
    }
    
    try:
        # Eğer varsa eski dosyayı sil
        if os.path.exists('indirilen_video.mp4'):
            os.remove('indirilen_video.mp4')
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return send_file('indirilen_video.mp4', as_attachment=True)
    except Exception as e:
        return f"Hata: {str(e)}"

if __name__ == '__main__':
    # Render port ayarı
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

