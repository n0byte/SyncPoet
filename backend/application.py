from mode import single_mode, c2m_mode, m2c_mode, all_mode
from datetime import datetime
from flask_cors import CORS
import threading
import flask
import json
import os

# Initialize Flask app
app = flask.Flask(__name__)
CORS(app)

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(current_dir, "cache")
jsoninput_dir = os.path.join(current_dir, "jsoninput.json")
info_dir = os.path.join(current_dir, "information.json")

# Create directories and files if they don't exist
os.makedirs(cache_dir, exist_ok=True)

# Create jsoninput.json with empty array if it doesn't exist
if not os.path.exists(jsoninput_dir):
    with open(jsoninput_dir, 'w') as f:
        json.dump([], f, indent=4)

# Create information.json with empty object if it doesn't exist
if not os.path.exists(info_dir):
    with open(info_dir, 'w') as f:
        json.dump({}, f, indent=4)


# ==================== Writes the Information from the Frontend or the fetch in the Json File and then it reads the Json File to 
# know the Mode that was written and then it executes the Funktion in the mode.py. The Funktion that get executed depens 
# on the Mode in the Json. And it locks any Input bevor the funktion is finished, when the Funktion ist not done its blocks all request.
# ==================== #
# Lock for synchronizing requests
request_lock = threading.Lock()

process_status = {
    "isRunning": False,
    "currentProcess": None,
    "startTime": None
}

@app.route('/api/getInformation', methods=['POST'])
def getInformation():
    global process_status
    
    # Check if process is already running
    if process_status["isRunning"]:
        return flask.jsonify({
            "status": "busy",
            "message": f"Process {process_status['currentProcess']} is running since {process_status['startTime']}",
            "processId": process_status['currentProcess']
        }), 503

    # Check if we can acquire the lock
    if not request_lock.acquire(blocking=False):
        return flask.jsonify({
            "status": "busy",
            "message": "Another process is trying to start"
        }), 503

    try:
        # Get data from request
        data = flask.request.get_json()
        
        # Update process status
        process_status["isRunning"] = True
        process_status["currentProcess"] = data.get('mode', 'unknown')
        process_status["startTime"] = datetime.now().strftime("%H:%M:%S")

        # Write data to information.json
        with open(info_dir, 'w') as f:
            json.dump(data, f)

        # Execute corresponding function based on mode
        mode = data.get('mode', '')
        result = None
        
        if mode == 'single':
            result = single_mode()
        elif mode == 'c2m':
            result = c2m_mode()
        elif mode == 'm2c':
            result = m2c_mode()
        elif mode == 'all':
            result = all_mode()
        else:
            return flask.jsonify({"error": "Invalid mode"}), 400

        return flask.jsonify({
            "status": "success",
            "result": result,
            "processDetails": {
                "startTime": process_status["startTime"],
                "endTime": datetime.now().strftime("%H:%M:%S")
            }
        })

    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500

    finally:
        # Reset process status
        process_status["isRunning"] = False
        process_status["currentProcess"] = None
        process_status["startTime"] = None
        # Release the lock
        request_lock.release()


# ==================== Gives the Frontend the information about the files in the cache directory and their status ==================== #
@app.route('/api/getSidebarinput', methods=['GET'])
def getjsoninput():
    try:
        with open(jsoninput_dir, "r") as file:
            data = json.load(file)
            formatted_data = [
                {
                    'filename': item.get('filename', 'Unknown'),
                    'status': item.get('status', 'Unknown')
                }
                for item in data if isinstance(item, dict)
            ]
        return flask.jsonify(formatted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return flask.jsonify([])
    


if __name__ == '__main__':
    app.run(port=5000, debug=True)