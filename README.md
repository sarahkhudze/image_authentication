# Secure Image Authentication System

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![RSA](https://img.shields.io/badge/Cryptography-413D3D?style=for-the-badge&logo=letsencrypt&logoColor=white)

A Django-based system that authenticates users and verifies image ownership using **EXIF metadata** and **hybrid cryptography** (RSA + AES).

## 🔐 Key Features

- **Biometric Registration**:  
  Users enroll with telephone, ID number, and their camera's EXIF signature
- **Image Fingerprinting**:  
  Prevents duplicate uploads across users via SHA-256 hashing
- **Cryptographic Verification**:  
  - RSA-2048 for key exchange  
  - AES-256 for image encryption
- **Tamper Detection**:  
  Validates images against original camera Make/Model from EXIF data

## ⚙️ Technical Stack

| Component          | Technology Used           |
|--------------------|---------------------------|
| Backend Framework  | Django 5.1                |
| Database           | SQLite (Dev) / PostgreSQL (Prod) |
| Cryptography       | `cryptography` + `rsa` libraries |
| Image Processing   | Pillow (EXIF extraction)  |
| Frontend           | Bootstrap 5 + Purple Theme |

## 🚀 Quick Setup

1. **Clone Repository**  
   ```bash
   git clone https://github.com/sarahkhudze/image_authentication/
   cd image_authentication

2. **Configure Environment**
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

3. **Initialize Database**
python manage.py migrate
python manage.py createsuperuser

4. **Run Development Server**
python manage.py runserver

**Project Structure**

ImageAuth/                      ← Root folder (contains manage.py)
├── authsystem/                 ← Main Django app
│   ├── static/                 ← Static files folder
│   │   └── authsystem/         ← Namespaced static files
│   │       ├── css/            ← CSS files (purple theme)
│   │       │   └── styles.css
│   │       └── js/             ← JavaScript files
│   │           └── script.js
│   ├── templates/              ← HTML templates
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   └── ... (other app files)
├── ImageAuth/                  ← Project config folder
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
└── requirements.txt            ← THIS FILE (in root with manage.py)
