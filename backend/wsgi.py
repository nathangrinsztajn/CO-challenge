import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app import app

application = app

if __name__ == "__main__":
    app.run()
