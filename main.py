import os
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from modules.hash import hash_file, verify_integrity
from modules.encryption import aes_encrypt, aes_decrypt, rsa_encrypt, rsa_decrypt
from modules.password import check_strength,hash_pw

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    result_text = ""
    try:
        choice = int(request.form.get('choice'))

        if choice == 1:
            if 'file1' not in request.files:
                return jsonify({'result': 'Error: No file part'}), 400
            file = request.files['file1']
            if file.filename == '':
                return jsonify({'result': 'Error: No selected file'}), 400
            
            filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result_text = f"SHA256: {hash_file(filepath)}"
            os.remove(filepath)

        elif choice == 2:
            if 'file1' not in request.files or 'file2' not in request.files:
                return jsonify({'result': 'Error: Two files are required'}), 400
            file1, file2 = request.files['file1'], request.files['file2']
            if file1.filename == '' or file2.filename == '':
                return jsonify({'result': 'Error: Two files must be selected'}), 400
            
            filename1 = f"{uuid.uuid4()}_{secure_filename(file1.filename)}"
            filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            file1.save(filepath1)

            filename2 = f"{uuid.uuid4()}_{secure_filename(file2.filename)}"
            filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            file2.save(filepath2)

            try:
                result_text = verify_integrity(filepath1, filepath2)
            finally:
                if os.path.exists(filepath1):
                    os.remove(filepath1)
                if os.path.exists(filepath2):
                    os.remove(filepath2)

        elif choice in [3, 4, 5, 6, 7]:
            val1 = request.form.get('val1')
            val2 = request.form.get('val2')

            if not val1:
                 return jsonify({'result': 'Error: Input value is required.'}), 400

            if choice == 3:
                key, ciphertext = aes_encrypt(val1.encode())
                result_text = f"AES Key: {key}\nCiphertext: {ciphertext}"
            elif choice == 4:
                result_text = f"Plaintext: {aes_decrypt(val1, val2)}"
            elif choice == 5:
                priv_key, ciphertext = rsa_encrypt(val1.encode())
                result_text = f"Private Key (Save this!):\n{priv_key}\nCiphertext: {ciphertext}"
            elif choice == 6:
                result_text = f"Plaintext: {rsa_decrypt(val1, val2)}"
            elif choice == 7:
                strength = check_strength(val1)
                hashed = hash_pw(val1)
                result_text = f"{strength}\nHashed: {hashed.decode()}"
        else:
            result_text = "Invalid option selected."
    except Exception as e:
        app.logger.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({'result': f"An unexpected server error occurred: {e}"}), 500
        
    return jsonify({'result': result_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)