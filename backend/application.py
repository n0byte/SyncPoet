import flask
from flask_cors import CORS
import json
import os
import atexit
from mode import single_mode, c2m_mode, m2c_mode, all_mode
import threading

app = flask.Flask(__name__)
CORS(app)

current_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(current_dir, "cache")
jsoninput_dir = os.path.join(current_dir, "jsoninput.json")
info_dir = os.path.join(current_dir, "information.json")

def clear_json_files():
    with open(jsoninput_dir, 'w') as f:
        json.dump([], f)
    with open(info_dir, 'w') as f:
        json.dump({}, f)

def update_json_files():
    while True:
        try:
            # Get current files in cache
            cache_files = [f for f in os.listdir(cache_dir) if os.path.isfile(os.path.join(cache_dir, f))]
            
            # Read current JSON content
            with open(jsoninput_dir, 'r') as f:
                current_data = json.load(f)
            
            # Get existing filenames
            existing_files = [item['filename'] for item in current_data if isinstance(item, dict)]
            
            # Add new files to JSON
            for file in cache_files:
                filename = os.path.splitext(file)[0]  # Remove extension
                if filename not in existing_files:
                    current_data.append({
                        'filename': filename,
                        'status': 'Clear'
                    })
            
            # Write updated data
            with open(jsoninput_dir, 'w') as f:
                json.dump(current_data, f)
                
            threading.Event().wait(1.0)  # Check every second
            
        except Exception as e:
            print(f"Error in file monitoring: {e}")
            threading.Event().wait(5.0)  # Wait 5 seconds on error

def init_files():
    clear_json_files()
    # Start file monitoring in background
    monitor_thread = threading.Thread(target=update_json_files, daemon=True)
    monitor_thread.start()

atexit.register(clear_json_files)
init_files()

# Global lock for synchronization
processing_lock = threading.Lock()
is_processing = False

# ==================== Writes the Information from the Frontend or the fetch in the Json File and then it reads the Json File to 
# know the Mode that was written and then it executes the Funktion in the mode.py. The Funktion that get executed depens 
# on the Mode in the Json. And it locks any Input bevor the funktion is finished, when the Funktion ist not done its blocks all request.
# ==================== #
@app.route('/api/writeInformation', methods=['POST'])
def write_information():
    global is_processing
    if is_processing:
        return flask.jsonify({"status": "busy", "message": "Another task is currently processing"}), 429

    try:
        data = flask.request.get_json()
        if not data or 'mode' not in data:
            return flask.jsonify({"status": "error", "message": "Invalid data format"}), 400

        with processing_lock:
            is_processing = True
            # Write to information.json
            with open(info_dir, 'w') as f:
                json.dump(data, f)

            # Execute corresponding mode function
            mode = data.get('mode')
            try:
                if mode == 'single':
                    result = single_mode()
                elif mode == 'c2m':
                    result = c2m_mode()
                elif mode == 'm2c':
                    result = m2c_mode()
                elif mode == 'all':
                    result = all_mode()
                else:
                    return flask.jsonify({"status": "error", "message": "Invalid mode"}), 400
                
                return flask.jsonify({"status": "success", "result": result})
            finally:
                is_processing = False

    except Exception as e:
        is_processing = False
        return flask.jsonify({"status": "error", "message": str(e)}), 500
    

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