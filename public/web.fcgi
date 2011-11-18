#!/usr/bin/python
import os
import sys

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_DIR)
sys.path.insert(0, os.path.dirname(_PROJECT_DIR))

import cli

if __name__ == "__main__":
    if sys.platform == "win32":
        cli.run(cli.app, host='localhost', port=8080, reloader=True)
    else:
        from flup.server.fcgi import WSGIServer
        WSGIServer(cli.app).run()
