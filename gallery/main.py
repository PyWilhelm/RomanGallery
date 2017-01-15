# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


def main():
    from views import views
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('host.crt', 'host.key'))
