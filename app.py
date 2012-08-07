from flask import Flask
from config import TEMPLATE_FOLDER, DEBUG, HOST, PORT
import controllers

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
