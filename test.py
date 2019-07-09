#!/usr/bin/env python3

from potnanny_api import create_app
from potnanny_api.config import Development
app = create_app(Development)

if __name__ == '__main__':
    app.run()
