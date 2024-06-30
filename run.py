from config import config
from flask import Flask
from app import createApp
from storage import Storage

app = Flask(__name__)
createApp(app,config)
Storage.init("data")

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 5000,debug=config.DEBUG)