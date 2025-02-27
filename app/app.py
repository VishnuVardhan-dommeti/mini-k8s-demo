from flask import Flask, jsonify
import os, socket, datetime

app = Flask(__name__)

APP_NAME = os.getenv('APP_NAME', 'mini-k8s-demo')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
request_count = 0

@app.route('/')
def index():
    global request_count
    request_count += 1
    return f"""
    <h1>Kubernetes Mini Demo</h1>
    <p>App: {APP_NAME} v{APP_VERSION}</p>
    <p>Pod: {socket.gethostname()}</p>
    <p>Requests: {request_count}</p>
    <p>Time: {datetime.datetime.now()}</p>
    """

@app.route('/api/health')
def health():
    return jsonify(status='healthy')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
