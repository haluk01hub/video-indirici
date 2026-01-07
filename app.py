from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Yeni Reklam Kodun Yerleştirilmiş Tasarım
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hızlı Video İndirici</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0f0f0f; color: #ffffff; text-align: center; padding: 10px; }
        .card { max-width: 500px; margin: 20px auto; background: #1a1a1a; padding: 25px; border-radius: 20px; border: 1px solid #333; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #000; color: white; margin-bottom: 20px; font-size: 16px; }
        button { width: 95%; padding: 15px; background: linear-gradient(45deg, #ff0000, #ff4444); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 16px; }
        .reklam-alani { margin: 20px auto; max-width: 500px; min-height: 150px; }
    </style>
</head>
<body>

    <div class="card">
        <h2>🚀 Video İndirici</h2>
        <p style="color: #aaa;">TikTok, Instagram ve YouTube videolarını indir!</p>
        
        <form action="/hazirla" method="post">
            <input type="text" name="url" placeholder="Video linkini buraya yapıştır..." required>
            <button type="submit">VİDEOYU İNDİR</button>
        </form>
    </div>

    <div class="reklam-alani">
        <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
        <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
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
