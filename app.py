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
    <title>Tik-Insta Save - HD Video İndirici</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #080808; color: white; text-align: center; padding: 10px; }
        .card { max-width: 450px; margin: 30px auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #222; }
        input { width: 90%; padding: 15px; border-radius: 10px; border: 1px solid #333; background: #000; color: white; margin-bottom: 20px; outline: none; }
        .btn { width: 100%; padding: 16px; border: none; border-radius: 12px; cursor: pointer; font-weight: bold; margin-bottom: 12px; font-size: 16px; }
        .btn-normal { background: #222; color: #888; }
        .btn-premium { background: linear-gradient(90deg, #ff0000, #b30000); color: white; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Tik-Insta Save</h1>
        <form action="/islem" method="post">
            <input type="url" name="url" placeholder="Video linkini yapıştır..." required>
            <button type="submit" name="mod" value="normal" class="btn btn-normal">HIZLI İNDİR (SD)</button>
            <button type="submit" name="mod" value="premium" class="btn btn-premium">✨ HD FİLİGRANSIZ (POP-UP REKLAM)</button>
        </form>
    </div>
    <script async="async" data-cfasync="false" src="https://pl28425178.effectivegatecpm.com/f3df8ed4d3c5858e1c187ea1227bc5ed/invoke.js"></script>
    <div id="container-f3df8ed4d3c5858e1c187ea1227bc5ed"></div>
</body>
</html>
'''

# REKLAMLI BEKLEME SAYFASI (Pop-up Entegreli)
WAIT_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hazırlanıyor...</title>
    <style>
        body { font-family: 'Inter', sans-serif; background: #000; color: white; text-align: center; margin: 0; overflow: hidden; }
        #popup-reklam { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: white; z-index: 9999; display: block; }
        .close-ad { position: absolute; top: 10px; right: 10px; background: #ff0000; color: white; padding: 5px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; z-index: 10000; }
        .main-content { padding-top: 50px; }
        #timer { font-size: 40px; color: #ff0000; font-weight: bold; }
        #indir-btn { display: none; margin: 20px auto; padding: 15px 30px; background: #28a745; color: white; border: none; border-radius: 10px; cursor: pointer; font-size: 18px; }
    </style>
</head>
<body>

    <div id="popup-reklam">
        <div class="close-ad" onclick="closeAd()">REKLAMI GEÇ [X]</div>
        <iframe src="https://www.effectivegatecpm.com/et6wj2f9?key=62e749d77eb3f45ce41046a596605850" style="width:100%; height:100%; border:none;"></iframe>
    </div>

    <div class="main-content">
        <h3>📽️ Videonuz Hazırlanıyor</h3>
        <p>Reklam bittiğinde indirme butonu açılacaktır.</p>
        <div id="timer">10</div>

        <form action="/indir_final" method="post">
            <input type="hidden" name="url" value="{{ url }}">
            <button type="submit" id="indir-btn">📥 HD VİDEOYU İNDİR</button>
        </form>
    </div>

    <script>
        let s = 10;
        function closeAd() {
            document.getElementById('popup-reklam').style.display = 'none';
            document.body.style.overflow = 'auto';
            startCountdown();
        }

        function startCountdown() {
            let i = setInterval(() => {
                s--;
                document.getElementById('timer').innerText = s;
                if(s <= 0) {
                    clearInterval(i);
                    document.getElementById('timer').style.display = 'none';
                    document.getElementById('indir-btn').style.display = 'block';
                }
            }, 1000);
        }
        
        // Otomatik kapatma uyarısı (opsiyonel)
        setTimeout(() => {
            alert("V
