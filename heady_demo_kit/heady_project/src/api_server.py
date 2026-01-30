from flask import Flask, jsonify
import os
import sys

# Ensure current directory is in path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Heady Demo Kit API Operational", "version": "1.0.0", "service": "heady-demo-kit"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
