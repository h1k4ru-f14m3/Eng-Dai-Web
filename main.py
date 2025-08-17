from app import app
from functions.roles import init_json, save_json
import atexit

atexit.register(save_json)

if __name__ == "__main__":
    init_json()
    app.run(host="0.0.0.0", port=5000)