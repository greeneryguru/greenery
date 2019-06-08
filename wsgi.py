#!/usr/bin/env python3

from potnanny_api import create_app
from potnanny_api.config import Production
app = create_app(Production)

if __name__ == '__main__':
    app.run()
