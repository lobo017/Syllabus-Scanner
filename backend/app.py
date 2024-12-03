from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import docxToTxt as dx
import pdfToTxt as px


app = Flask(__name__)
CORS(app)

upload_folder = '../uploads'
parsed_folder = '../parsed'
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(parsed_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['PARSED_FOLDER'] = parsed_folder


@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for upload"}), 400

    # Save the uploaded file
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(upload_path)

    # Determine file type and parse accordingly
    file_extension = file.filename.split('.')[-1].lower()
    parsed_filename = f"{os.path.splitext(file.filename)[0]}.txt"
    parsed_path = os.path.join(app.config['PARSED_FOLDER'], parsed_filename)

    try:
        if file_extension == 'docx':
            dx.parse_docx(upload_path, parsed_path)
        elif file_extension == 'pdf':
            px.parse_pdf(upload_path, parsed_path)
        else:
            return jsonify({"error": f"Unsupported file type: {file_extension}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": f"File parsed successfully: {parsed_filename}",
                    "parsed_path": parsed_path}), 200
    


if __name__ == '__main__':
    app.run(debug=True)