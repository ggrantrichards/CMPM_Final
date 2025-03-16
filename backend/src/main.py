from flask import Flask, request, jsonify, send_from_directory, send_file, Response, stream_with_context
from build_generator import generate_build
import sys
import os
import time
import base64

# Initialize Flask app with the correct static and template folders
dist_dir = os.path.join(os.path.dirname(__file__), '../../frontend/Client/dist')
app = Flask(
    __name__, 
    static_folder=dist_dir,
    template_folder=dist_dir
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Store the build status
build_status = {"status": "IDLE"}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    else:
        return send_from_directory(dist_dir, 'index.html')

# Serve static files (CSS, JS)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Handle build generation requests.
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    size = int(data['size'])
    description = data['description'].strip()
    build_type = description.lower().replace(" ", "_")

    def generate_and_stream():
        global build_status
        build_status["status"] = "IN_PROGRESS"
        for _ in generate_build(size, description, build_type):
            pass
        # Notify the frontend that the build is complete
        build_status["status"] = "COMPLETE"
        yield f"data: BUILD_COMPLETE\n\n"

    # Return the response with stream_with_context
    return Response(stream_with_context(generate_and_stream()), mimetype='text/event-stream')

# SSE endpoint to stream build status updates
@app.route('/build-status')
def build_status_stream():
    def generate():
        while True:
            yield f"data: {build_status['status']}\n\n"
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')

# List previously generated builds
@app.route('/list-builds', methods=['GET'])
def list_builds():
    builds = []
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output')
    if os.path.exists(output_path):
        for folder in os.listdir(output_path):
            if os.path.isdir(os.path.join(output_path, folder)):
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

    build_path = os.path.join(os.path.dirname(__file__), '..', 'output', folder)
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

    build_path = os.path.join(os.path.dirname(__file__), '..', 'output', folder)
    if not os.path.exists(build_path):
        return jsonify({"error": "Build not found"}), 404

    # Look for the .schem file in the build folder
    schematic_file = None
    for file in os.listdir(build_path):
        if file.endswith('.schem'):
            schematic_file = file
            break

    if not schematic_file:
        return jsonify({"error": "Schematic file not found"}), 404

    schematic_path = os.path.join(build_path, schematic_file)
    return send_file(schematic_path, as_attachment=True)

if __name__ == '__main__':
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    app.run(debug=True, port=8080)