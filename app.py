from flask import Flask, request, redirect, render_template_string
import re
import os

app = Flask(__name__)

# Página inicial para exibir uma mensagem
@app.route('/')
def home():
    return "GET USER VIP"

# Função de redirecionamento
@app.route('/get-video/mxfliofc-vip/<path:url>', methods=['GET'])
def redirect_video(url):
    try:
        # Extrair a parte relevante da URL
        match = re.match(r'https://(.+)/e/(.+)', url)
        if not match:
            return "Invalid URL format", 400
        
        base_url = match.group(1)
        video_id = match.group(2)
        new_url = f"https://{base_url}/f/{video_id}_x"
        
        # Redirecionar para a nova URL
        return redirect(new_url, code=302)
    except Exception as e:
        return str(e), 500

# Funções para a funcionalidade do YouTube
def extract_video_id(url):
    video_id = None
    if 'youtube.com' in url:
        match = re.search(r'v=([^&]+)', url)
        if match:
            video_id = match.group(1)
    elif 'youtu.be' in url:
        match = re.search(r'youtu\.be/([^?]+)', url)
        if match:
            video_id = match.group(1)
    return video_id

@app.route('/yout/mx/url', methods=['POST'])
def video():
    youtube_url = request.form.get('url')
    return handle_video_request(youtube_url, redirect_to_index=True)

@app.route('/yout/mx/URL/<path:youtube_url>')
def video_from_path(youtube_url):
    youtube_url = youtube_url.replace(":/", "://")
    return handle_video_request(youtube_url, redirect_to_index=False)

def handle_video_request(youtube_url, redirect_to_index):
    if youtube_url:
        video_id = extract_video_id(youtube_url)
        if video_id:
            try:
                youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                yt = YouTube(youtube_url)
                video_stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
                video_url = video_stream.url
                if redirect_to_index:
                    return redirect(url_for('index', video_url=video_url))
                else:
                    return redirect(video_url)
            except Exception as e:
                error_message = "Failed to load the video. Please try again."
                if redirect_to_index:
                    return redirect(url_for('index', error=error_message))
                else:
                    return render_template_string(TEMPLATE, video_url=None, error=error_message)
    error_message = "Invalid URL. Please enter a valid YouTube URL."
    if redirect_to_index:
        return redirect(url_for('index', error=error_message))
    else:
        return render_template_string(TEMPLATE, video_url=None, error=error_message)

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Video Player</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            color: white;
        }
        h1 {
            color: white;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 16px;
            width: 300px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 15px;
            font-size: 16px;
            color: #fff;
            background-color: #007BFF;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        video {
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .loader {
            border: 16px solid #f3f3f3;
            border-radius: 50%;
            border-top: 16px solid #3498db;
            width: 120px;
            height: 120px;
            animation: spin 2s linear infinite;
            margin-top: 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <h1>NA MX, VOCÊ NÃO VERÁ ADS</h1>
    <form id="videoForm" action="/yout/mx/url" method="post">
        <input type="text" name="url" placeholder="Enter YouTube video URL" required>
        <button type="submit">Play Video</button>
    </form>
    <div id="loader" class="loader" style="display:none;"></div>
    <div id="videoContainer" style="display:{{ 'block' if video_url else 'none' }};">
        {% if video_url %}
            <video controls width="600">
                <source src="{{ video_url }}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        {% elif error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
    <script>
        document.getElementById('videoForm').addEventListener('submit', function() {
            document.getElementById('loader').style.display = 'block';
            document.getElementById('videoContainer').style.display = 'none';
        });
        window.onload = function() {
            if ("{{ video_url }}") {
                document.getElementById('loader').style.display = 'none';
                document.getElementById('videoContainer').style.display = 'block';
            }
        };
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
                
