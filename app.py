from flask import Flask, render_template, request, send_file, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

downloads_path = os.path.join(os.path.dirname(__file__), 'downloads')
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/terabox')
def terabox():
    return render_template('terabox.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    url = request.form['url']
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [f for f in info['formats'] if f.get('ext') == 'mp4']
    return render_template('quality.html', formats=formats, video_url=url, title=info['title'])

@app.route('/download', methods=['POST'])
def download():
    format_id = request.form['format_id']
    url = request.form['url']
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s')
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
