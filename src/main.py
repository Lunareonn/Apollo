from frontend.site import app, socketio
from backend.util import generate_config, check_if_running
import webbrowser
import tempfile
import os
import atexit

def exit_handler():
    pid_file = os.path.join(tempfile.gettempdir(), "apollo.pid")
    if os.path.isfile(pid_file):
        os.remove(pid_file)
        print("deleted pid file")

def main():
    is_running = check_if_running()
    if is_running:
        webbrowser.open("http://127.0.0.1:5000", new=2)
        return
    
    with open(os.path.join(tempfile.gettempdir(), "apollo.pid"), "w") as f:
        f.write(str(os.getpid()))

    atexit.register(exit_handler)
    generate_config()
    webbrowser.open("http://127.0.0.1:5000", new=2)
    socketio.run(app, debug=False)

if __name__ == "__main__":
    main()
