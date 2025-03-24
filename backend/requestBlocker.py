import threading

blocker_status = False
lock = threading.Lock()

def check_blocker_status():
    with lock:
        return blocker_status

def activate_blocker():
    global blocker_status
    with lock:
        blocker_status = True

def deactivate_blocker():
    global blocker_status
    with lock:
        blocker_status = False