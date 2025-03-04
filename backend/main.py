from flask import Flask, request, jsonify, send_from_directory
from build_generator import generate_build
import os

app = Flask(__name__)

# Serve the frontend (index.html)
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

# Handle build generation requests
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    size = int(data['size'])
    build_type = data['type']

    # Generate the build
    generate_build(size, build_type)

    return jsonify({"status": "success", "message": "Build generated successfully!"})

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    app.run(debug=True)