import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# Vercel için handler
def handler(request, response):
    return app(request, response)

# ASGI application export
application = app