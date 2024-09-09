from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

# Import routes after creating the app instance
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
