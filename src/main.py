from frontend.site import app, socketio
from backend.util import generate_config

def main():
    generate_config()
    socketio.run(app, debug=True)
    # app.run(debug=True, host="0.0.0.0", threaded=True)

if __name__ == "__main__":
    main()
