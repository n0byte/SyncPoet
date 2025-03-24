from requestBlocker import check_blocker_status, activate_blocker, deactivate_blocker
from mode import single_mode, c2m_mode, m2c_mode, all_mode
from flask import Flask, request, jsonify
from jsonReader import GETmode, modeInfo_dir, sidebarInfo_dir
from jsonWriter import writeModeInformation
import threading
import json
import time

app = Flask(__name__)

def routes(app):

    @app.route('/GETmodeInfo', methods=['GET'])
    def mode_execusion():
        # Check if the request is blocked
        if check_blocker_status():
            return jsonify({"error": "Request is blocked, try again later."}), 403

        # Writing mode info into the modeInfo.json file
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Schreiben in JSON-Datei
        writeModeInformation(data)

        # Aktivate the request blocker
        activate_blocker()
        print("Blocker activated.")

        # Function to select the mode
        def modeSelection():
            mode = GETmode()
            print(f"Mode read from file: {mode}")

            if mode == "single":
                single_mode()
            elif mode == "c2m":
                c2m_mode()
            elif mode == "m2c":
                m2c_mode()
            elif mode == "all":
                all_mode()
            else:
                print("Invalid mode selected.")

            # Deactivate the request blocker
            deactivate_blocker()
            print("Blocker deactivated.")

        # Start the mode selection in a new thread
        threading.Thread(target=modeSelection, daemon=True).start()

        # Return the response
        return jsonify({"status": "success", "message": "Data written and blocker activated."})


@app.route('/api/GETsidebarInfo', methods=['GET'])
def send_sidebar_info():
    try:
        with open(sidebarInfo_dir, "r") as file:
            data = json.load(file)
            formatted_data = [
                {
                    'filename': item.get('filename', 'Unknown'),
                    'status': item.get('status', 'Unknown')
                }
                for item in data if isinstance(item, dict)
            ]
        return jsonify(formatted_data), 200, {'Content-Type': 'application/json'}
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify([]), 404, {'Content-Type': 'application/json'}