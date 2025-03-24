from flask_cors import CORS
from ensure import ensure
from rout import routes
from flask import Flask
import logging
import socket

logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)

# Routen aus rout.py registrieren
routes(app)

def get_local_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def run():
    if ensure():
        local_ip = get_local_ip()
        port = 5000
        print("Passed ensure. Starting server...")
        print(f"Server is running at:")
        print(f"- Local:   http://localhost:{port}")
        print(f"- Network: http://{local_ip}:{port}")
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    else:
        print("Ensure failed. Exiting...")
        print("failed to start server...") 

if __name__ == '__main__':
    run()