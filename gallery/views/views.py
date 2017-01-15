# -*- coding: utf-8 -*-
from gallery.main import app

@app.route('/')
def main_handler():
    return 'hello world'