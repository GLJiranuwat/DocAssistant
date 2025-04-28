import os
from flask import Flask, request, send_from_directory, jsonify, url_for, make_response
import json
from jinja2 import Template

app = Flask(__name__)

# ใช้ /tmp directory สำหรับ Vercel
OUTPUT_FOLDER = '/tmp'  # Vercel ใช้ /tmp สำหรับการเขียนไฟล์ชั่วคราว

with open('template.html', encoding='utf-8') as f:
    template_html = f.read()

template = Template(template_html)

@app.route('/generate-form', methods=['POST'])
def generate_form():
    try:
        form_data_bytes = request.data
        print("form data byte:", form_data_bytes)
        form_data_str = form_data_bytes.decode('utf-8').strip()
        print("form data string", form_data_str)
        form_data = json.loads(form_data_str)
        print("form data json:", form_data)

        rendered_html = template.render(form_data=form_data)

        filename = 'filled_form.html'
        filepath = os.path.join(OUTPUT_FOLDER, filename)

        # เขียนไฟล์ไปยัง /tmp
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        # ใช้ url_for เพื่อให้ได้ URL สำหรับการดาวน์โหลด
        download_url = url_for('download_file', filename=filename, _external=True)

        return jsonify({"download_url": download_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        # ใช้ /tmp directory
        return send_from_directory(OUTPUT_FOLDER, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
