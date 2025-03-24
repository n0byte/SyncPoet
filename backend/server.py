from flask_cors import CORS
from ensure import ensure
from rout import routes
from flask import Flask
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)

# Routen aus rout.py registrieren
routes(app)

def run():
    if ensure():
        print("Passed ensure. Starting server...")
        app.run(port=5000, debug=False, use_reloader=False)
        print("Server is running...")
    else:
        print("Ensure failed. Exiting...")
        print("failed to start server...") 

if __name__ == '__main__':
    run()