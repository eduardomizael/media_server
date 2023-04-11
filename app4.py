from flask import Flask, render_template, send_from_directory, render_template_string, send_file, redirect, url_for
from pathlib import Path


app = Flask(__name__)


# Define o diretório que contém as mídias (imagens e vídeos)
MEDIA_FOLDER = r'Z:\Projects\media_server2\static'
MEDIA_PATH = Path(MEDIA_FOLDER)
FILE_SOURCES = list(MEDIA_PATH.glob('*'))

FILE_SOURCE = r'Z:\Projects\media_server\static\video.mp4'

@app.route('/')
def index():
    return render_template('index.html', file_index=0)


@app.route('/video/<int:file_index>')
def video(file_index):
    if file_index > (len(FILE_SOURCES) - 1):
        return redirect(url_for('video', file_index=0))

    return render_template('index.html', file=FILE_SOURCES[file_index].name, file_index=file_index)


@app.route('/next_file')
def next_file():
    return FILE_SOURCE


@app.route('/video_file')
def video_file():
    return send_file(FILE_SOURCE, mimetype='video/mp4')


if __name__ == '__main__':
    # Executa o servidor Flask na porta 5000
    app.run(debug=True, port=5000)
