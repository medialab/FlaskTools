from flask import Flask
from config import TEMPLATE_FOLDER, DEBUG, HOST, PORT

app = Flask('tools', template_folder=TEMPLATE_FOLDER)
import controllers

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
