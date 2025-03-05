from flask import Flask, request, jsonify, send_from_directory, send_file
from build_generator import generate_build
import os
import json

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

# List previously generated builds
@app.route('/list-builds', methods=['GET'])
def list_builds():
    builds = []
    if os.path.exists('output'):
        for folder in os.listdir('output'):
            if os.path.isdir(os.path.join('output', folder)):
                print(f"Found folder: {folder}")  # Debug statement
                parts = folder.split('_', 2)  # Split into 3 parts at most
                if len(parts) == 3:
                    build_type, size, timestamp = parts
                    print(f"Parsed: type={build_type}, size={size}, timestamp={timestamp}")  # Debug statement
                    builds.append({
                        "folder": folder,
                        "type": build_type,
                        "size": size.split('x')[0],  # Extract size (e.g., "10x10" -> "10")
                        "timestamp": timestamp  # Keep the full timestamp
                    })
                else:
                    print(f"Skipping folder due to incorrect format: {folder}")  # Debug statement
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

# Download schematic file
@app.route('/download-schematic', methods=['GET'])
def download_schematic():
    folder = request.args.get('folder')
    if not folder:
        return jsonify({"error": "Folder not specified"}), 400

    build_path = os.path.join('output', folder)
    if not os.path.exists(build_path):
        return jsonify({"error": "Build not found"}), 404

    schematic_file = f"{folder}.schem"
    schematic_path = os.path.join(build_path, schematic_file)
    if not os.path.exists(schematic_path):
        return jsonify({"error": "Schematic file not found"}), 404

    return send_file(schematic_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    app.run(debug=True)