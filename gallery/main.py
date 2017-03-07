# -*- coding: utf-8 -*-
from views import views


def main():
    views.app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
