from flask import Flask, render_template_string
from pytube import YouTube
import re

app = Flask(__name__)

def get_youtube_video_url(youtube_url):
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.get_highest_resolution()
        return stream.url
    except Exception as e:
        return None

@app.route('/URL/<path:youtube_path>')
def play_video(youtube_path):
    youtube_url = youtube_path.replace(":/", "://")  # Corrige a URL
    video_url = get_youtube_video_url(youtube_url)
    if not video_url:
        return "Erro ao carregar o vídeo.", 400

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Player</title>
        <style>
            body {{
                background: black;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            video {{
                width: 90%;
                max-width: 1080px;
                border: 4px solid white;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <video controls autoplay>
            <source src="{video_url}" type="video/mp4">
            Seu navegador não suporta vídeo.
        </video>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
