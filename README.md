# CyberKit

CyberKit is a comprehensive, web-based cybersecurity toolkit built with Python (Flask) and JavaScript. It provides a modern "hacker terminal" interface for performing various cryptographic and security operations locally on your machine.

## Features

- **File Operations**:
  - **Hash File**: Calculate SHA-256 hashes of uploaded files.
  - **Verify Integrity**: Compare two files to check if they are identical.
- **Symmetric Encryption**:
  - **AES Encrypt**: Encrypt text messages using AES-256-GCM.
  - **AES Decrypt**: Decrypt messages using the generated hex key.
- **Asymmetric Encryption**:
  - **RSA Encrypt**: Encrypt messages using RSA-2048 (OAEP padding).
  - **RSA Decrypt**: Decrypt messages using a generated PEM private key.
- **Analysis**:
  - **Password Strength**: Audit password complexity using `zxcvbn` and `bcrypt`.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cyberkit.git
   cd cyberkit
   ```

2. **Set up a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask cryptography zxcvbn bcrypt
   ```

## Usage

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Access the interface**
   Open your web browser and navigate to:
   `http://127.0.0.1:5000`

The application runs locally, and file uploads are processed in a temporary folder that is cleaned up automatically.