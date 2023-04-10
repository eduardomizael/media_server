import random

from flask import Flask, render_template, send_from_directory, render_template_string, send_file
import os
from pathlib import Path


app = Flask(__name__)


# Define o diretório que contém as mídias (imagens e vídeos)
MEDIA_FOLDER = r'static'
MEDIA_PATH = Path(MEDIA_FOLDER)

FILE_SOURCE = r'Z:\Projects\media_server\static\video.mp4'


@app.route('/')
def index():
    return render_template('index.html')


def get_media_from_index(index=None):
    media_files = list(Path(MEDIA_FOLDER).glob('*'))
    if not index:
        index = random.randrange(0, len(media_files)-1)
    return media_files[index]


@app.route('/video_file')
def video_file():
    return send_file(FILE_SOURCE, mimetype='video/mp4')


def content_template():
    content_path = get_media_from_index(1)
    content = f'''<video src="{content_path}" autoplay loop></video>'''

    return render_template_string(content)


@app.route('/media/<path:filename>')
def media(filename):
    # Retorna o arquivo de mídia solicitado pelo cliente
    return send_from_directory(MEDIA_FOLDER, filename)


if __name__ == '__main__':
    # Executa o servidor Flask na porta 5000
    app.run(debug=True, port=5000)