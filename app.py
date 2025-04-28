from flask import Flask, request, send_from_directory, jsonify, url_for, make_response
import os
import json
from jinja2 import Template

app = Flask(__name__)

OUTPUT_FOLDER = 'output_files'

# ต้องแน่ใจว่าโฟลเดอร์ output_files มีอยู่
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

with open('template.html', encoding='utf-8') as f:
    template_html = f.read()

template = Template(template_html)

@app.route('/generate-form', methods=['POST'])
def generate_form():
    try:
        form_data_bytes = request.data
        form_data_str = form_data_bytes.decode('utf-8')
        form_data = json.loads(form_data_str)

        rendered_html = template.render(form_data=form_data)

        filename = 'filled_form.html'
        filepath = os.path.join(OUTPUT_FOLDER, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        download_url = url_for('download_file', filename=filename, _external=True)

        return jsonify({"download_url": download_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        response = make_response(send_from_directory(OUTPUT_FOLDER, filename))
        # ใส่ header ngrok-skip-browser-warning ให้ทุก response
        response.headers['ngrok-skip-browser-warning'] = '1'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 404

app = app
