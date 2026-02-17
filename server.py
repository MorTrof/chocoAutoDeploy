from flask import Flask
import subprocess 
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "Сайт работает"

if __name__ == "__main__":
    app.run(host="192.168.1.77", port=80)
 