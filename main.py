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


class Librarian(App):
    def build(self):
        inipath = os.path.join(projpath, 'local.ini')
        server = threading.Thread(target=app.main,
                                  kwargs={'conf': inipath})
        server.setDaemon(True)
        server.start()
        return Label(text='Librarian v%s started' % __version__)


if __name__ == '__main__':
    Librarian().run()
