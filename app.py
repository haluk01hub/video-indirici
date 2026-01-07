from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Modern ve Reklam Alanlı Tasarım
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video İndirici - Hızlı ve Ücretsiz</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #121212; color: white; text-align: center; padding: 50px; }
        .container { max-width: 600px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        input { width: 80%; padding: 12px; border-radius: 5px; border: none; margin-bottom: 20px; }
        button { padding: 12px 25px; background-color: #ff0000; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #cc0000; }
        .reklam { margin: 20px 0; min-height: 100px; background: #2a2a2a; display: flex; align-items: center; justify-content: center; border: 1px dashed #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Video İndirici</h1>
        <p>YouTube, Instagram, TikTok videolarını anında indir.</p>
        
        <div class="reklam">
            <p style="color: #666;">Reklam Alanı</p>
        </div>

        <form action="/hazirla" method="post">
            <input type="text" name="url" placeholder="Video linkini buraya yapıştır..." required>
            <br>
            <button type="submit">VİDEOYU HAZIRLA</button>
        </form>

        <div class="reklam">
            <p style="color: #666;">Reklam Alanı</p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/hazirla', methods=['post'])
def hazirla():
    video_url = request.form.get('url')
    
    # FORMAT HATASINI ÇÖZEN AYARLAR
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'indirilen_video.mp4',
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return send_file('indirilen_video.mp4', as_attachment=True)
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
