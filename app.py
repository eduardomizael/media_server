import os
from flask import Flask, render_template, send_from_directory, render_template_string, send_file, redirect, url_for
from pathlib import Path


app = Flask(__name__)


# Define o diretório que contém as mídias (imagens e vídeos)
BASE_DIR = Path.cwd()

MEDIA_FOLDER = r'static'

MEDIA_PATH = BASE_DIR / MEDIA_FOLDER
# FILE_SOURCES = list(MEDIA_PATH.glob('*'))


@app.route('/')
def index():
    return render_template('index.html', )


@app.route('/video/<int:file_index>')
def video(file_index):
    files = list(MEDIA_PATH.glob('*'))
    try:
        file = files[file_index]
    except IndexError:
        if file_index == 0:
            return redirect(url_for('index'))
        return redirect(url_for('video', file_index=0))

    return render_template('media_player.html', file=file.name, file_index=file_index)


if __name__ == '__main__':
    # Executa o servidor Flask na porta 5000
    app.run(debug=True, port=5000)
