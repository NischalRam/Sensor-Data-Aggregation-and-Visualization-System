from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Make a request to your ESP32 API endpoint
    api_url = 'http://192.168.4.1'
    response = requests.get(api_url)
    data = response.json() if response.status_code == 200 else {}

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
