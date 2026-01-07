from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Reklam Kodun Yerleştirilmiş Modern Tasarım
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video İndirme Merkezi</title>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0f0f0f; color: #ffffff; text-align: center; padding: 20px; }
        .card { max-width: 500px; margin: 40px auto; background: #1a1a1a; padding: 30px; border-radius: 20px; border: 1px solid #333; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #000; color: white; margin-bottom: 20px; }
        button { width: 95%; padding: 15px; background: linear-gradient(45deg, #ff0000, #ff4444); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; }
        .footer { margin-top: 50px; color: #555; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Video İndirici</h2>
        <p style="color: #aaa;">YouTube, Instagram ve TikTok videolarını indir!</p>

        <form action="/hazirla" method="post">
            <input type="text" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit">VİDEOYU İNDİR</button>
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
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'indirilen_video.mp4',
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return send_file('indirilen_video.mp4', as_attachment=True)
    except Exception as e:
        return f"Hata: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


