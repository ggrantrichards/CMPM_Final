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
    description = data['description'].strip()

    # Generate the build using the free-text description.
    generate_build(size, description)

    return jsonify({"status": "success", "message": "Build generated successfully!"})

@app.route('/list-builds', methods=['GET'])
def list_builds():
    builds = []
    if os.path.exists('output'):
        for folder in os.listdir('output'):
            if os.path.isdir(os.path.join('output', folder)):
                # Expected folder format: {safe_description}_{size}x{size}_{timestamp}
                parts = folder.split('_', 2)
                if len(parts) == 3:
                    build_desc, size, timestamp = parts
                    builds.append({
                        "folder": folder,
                        "description": build_desc,
                        "size": size.split('x')[0],
                        "timestamp": timestamp
                    })
    return jsonify({"builds": builds})

# Load a specific build
@app.route('/load-build', methods=['GET'])
def load_build():
    folder = request.args.get('folder')
    if not folder:
        return jsonify({"error": "Folder not specified"}), 400

    build_path = os.path.join('output', folder)
    if not os.path.exists(build_path):
        return jsonify({"error": "Build not found"}), 404

    layers = []
    for file in sorted(os.listdir(build_path)):
        if file.startswith('layer_') and file.endswith('.txt'):
            with open(os.path.join(build_path, file), 'r') as f:
                layer = [line.strip().split(' ') for line in f.readlines()]
                layers.append(layer)

    return jsonify({"layers": layers})

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    app.run(debug=True)
