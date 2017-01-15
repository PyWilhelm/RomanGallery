# -*- coding: utf-8 -*-
from flask import request

from gallery.main import app


@app.route('/')
def main_handler():
    data = request.data
    print data
    return ''
