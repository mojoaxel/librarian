import os
import sys
import threading

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label

modpath = os.path.abspath(__file__)
projpath = os.path.dirname(modpath)
vendorpath = os.path.join(projpath, 'vendor')

sys.path.insert(0, vendorpath)

from librarian import __version__, app


def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


class Librarian(App):
    def build(self):
        ensure_dir('tmp/downloads/content')
        ensure_dir('tmp/downloads/files')
        ensure_dir('tmp/outernet')
        ensure_dir('tmp/zipballs')

        server = threading.Thread(target=app.main,
                                  kwargs={'conf': 'local.ini'})
        server.setDaemon(True)
        server.start()
        return Label(text='Librarian v%s started' % __version__)


if __name__ == '__main__':
    Librarian().run()
