import os
from flask import Flask, render_template, send_from_directory, render_template_string, send_file, redirect, url_for
from pathlib import Path
from waitress import serve
import json


class Config:
    media_folder: Path = Path('static')
    extensions: dict = {
        'video': ['.mp4', '.ogg', '.avi'],
        'image': ['.jpg', '.jpeg', '.gif', '.png', '.webp']
    }
    img_transition_time: int = 30
    __media_files: list = []

    def __init__(self, **kwargs):
        properties = [prop for prop in dir(self) if not prop.startswith('__')]
        for prop in properties:
            setattr(self, prop, getattr(self, prop))

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.__file = Path('config.json')
        # if not self.__file.exists():
        #     self.save_config()
        # else:
        #     self.load_config()

    def save_config(self):
        properties = [prop for prop in dir(self) if not prop.startswith('__')]
        with open(self.__file, 'w') as f:
            json.dump(properties, f, indent=4)

    def load_config(self):
        if not self.__file.exists():
            return self.save_config()
        cfg = json.load(open(self.__file, 'r'))
        for key, value in cfg.items():
            setattr(self, key, value)

    def get_media_files(self) -> list[dict[str, str, str]]:
        """Retorna uma lista de arquivos de mídia
        :return: Lista um dicionário com as informações dos arquivos de mídia no formato:
            [   {'index': 0, 'name': 'video.mp4', 'type': 'video'}, ...   ]
        """
        files = self.media_folder.glob('*')
        video_ext = self.extensions['video']
        image_ext = self.extensions['image']

        media_files = []
        for i, file in enumerate(files):
            if file.suffix in video_ext:
                media_files.append({'index': i, 'name': file.name, 'type': 'video'})
            elif file.suffix in image_ext:
                media_files.append({'index': i, 'name': file.name, 'type': 'image'})
        self.__media_files = media_files
        return media_files


    def get_file_from_index(self, file_index=0, retry=False) -> dict[str, str] | None:
        """Retorna um arquivo de mídia a partir de um índice
        :param file_index: Índice do arquivo de mídia
        :param retry: Se deve tentar novamente caso não exista arquivo de mídia
        :return: Dicionário com as informações do arquivo de mídia ou None caso não exista arquivo de mídia
        """
        media_files = self.__media_files
        if len(media_files) == 0:
            if retry:
                return None
            self.get_media_files()
            return self.get_file_from_index(file_index, True)
        if file_index in (range(len(media_files))):
            return media_files[file_index]
        self.get_media_files()
        return media_files[0]


config = None
app = None


def setup():
    global config, app

    config = Config()

    app = Flask(__name__)

    app.static_folder = config.media_folder

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/media/<int:file_index>')
    def media(file_index):
        file = config.get_file_from_index(file_index)
        itt = config.img_transition_time

        if not file:
            return redirect(url_for('index'))

        context = {
            'file_index': file.get('index'),
            'file_name': file.get('name'),
            'file_type': file.get('type'),
        }
        return render_template('media_player.html', file_index=file['index'], file_name=file['name'],
                               file_type=file['type'], itt=itt)

    return app


if __name__ == '__main__':
    # Executa o servidor Flask na porta 5000
    print('Executando o servidor')
    # app.run(debug=True, port=8000)
    # waitress-serve --listen 10.5.100.38:8000 app:app
    setup()
    serve(app, host='*', port=8000)
