from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return "GET USER VIP"

@app.route('/get-video/mxfliofc-vip/<path:url>')
def redirect_video(url):
    if url.startswith("https://wishonly.site/e/"):
        video_id = url.split("/")[-1]
        new_url = f"https://wishonly.site/f/{video_id}_x"
        return redirect(new_url)
    else:
        return "Formato de URL inválido", 400

if __name__ == '__main__':
    app.run(debug=False)
