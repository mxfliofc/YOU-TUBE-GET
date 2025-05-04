from flask import Flask, request, render_template_string, redirect, url_for
from pytube import YouTube
import re
import os
import urllib.parse

app = Flask(__name__)

def extract_video_id(url):
    if 'youtube.com' in url:
        match = re.search(r'v=([^&]+)', url)
        if match:
            return match.group(1)
    elif 'youtu.be' in url:
        match = re.search(r'youtu\.be/([^?]+)', url)
        if match:
            return match.group(1)
    return None

@app.route('/')
def index():
    video_url = request.args.get('video_url')
    error = request.args.get('error')
    return render_template_string(TEMPLATE, video_url=video_url, error=error)

@app.route('/yout/mx/url', methods=['POST'])
def video():
    youtube_url = request.form.get('url')
    return handle_video_request(youtube_url, redirect_to_index=True)

@app.route('/yout/mx/URL/<path:youtube_url>')
def video_from_path(youtube_url):
    decoded_url = urllib.parse.unquote(youtube_url)
    return handle_video_request(decoded_url, redirect_to_index=False)

def handle_video_request(youtube_url, redirect_to_index):
    if youtube_url:
        video_id = extract_video_id(youtube_url)
        if video_id:
            try:
                full_url = f"https://www.youtube.com/watch?v={video_id}"
                yt = YouTube(full_url)
                video_stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
                video_url = video_stream.url
                if redirect_to_index:
                    return redirect(url_for('index', video_url=video_url))
                else:
                    return redirect(video_url)
            except Exception as e:
                error_message = f"Erro ao carregar o vídeo: {str(e)}"
                if redirect_to_index:
                    return redirect(url_for('index', error=error_message))
                else:
                    return error_message
    error_message = "URL inválida. Forneça uma URL válida do YouTube."
    if redirect_to_index:
        return redirect(url_for('index', error=error_message))
    else:
        return error_message

# TEMPLATE (mesmo HTML que você já forneceu, mantido intacto)
TEMPLATE = """<html> ... </html>"""  # Deixe o HTML completo como no seu código original

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
