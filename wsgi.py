#!/usr/bin/env python3

from potnanny import create_app
from potnanny.config import Production
app = create_app(Production)

if __name__ == '__main__':
    app.run()
