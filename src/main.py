from frontend.site import app
from backend.util import generate_config

def main():
    generate_config()
    app.run(debug=True, host="0.0.0.0", threaded=True)

if __name__ == "__main__":
    main()
