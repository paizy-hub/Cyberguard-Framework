# Chipperhub - Substitution Cipher Application

## Project Overview

Chipperhub is a comprehensive desktop application developed for educational purposes, providing a secure and user-friendly platform for text encryption and decryption using the Substitution Cipher method.

## Features

- 🔐 Secure User Authentication System
- 🔒 Password Hashing with BCrypt
- 🔤 Substitution Cipher Encryption/Decryption
- 📋 Clipboard Integration (Copy/Paste Functionality)
- 🖥️ Intuitive Tkinter-based User Interface

## System Requirements

### Hardware Requirements
- Processor: 1 GHz or faster
- RAM: Minimum 2 GB
- Disk Space: 100 MB free space

### Software Requirements
- Python 3.8 or higher
- XAMPP (or MySQL Server)
- Git (optional, for cloning repository)

## Installation Guide

### Preparation

#### Windows Installation

1. **Install Python**
   - Download Python from [Official Python Website](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation by opening Command Prompt and running:
     ```
     python --version
     pip --version
     ```

2. **Install XAMPP**
   - Download XAMPP from [Apache Friends](https://www.apachefriends.org/)
   - Install XAMPP
   - Start Apache and MySQL modules from XAMPP Control Panel

3. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/chipperhub.git
   cd chipperhub
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

#### Linux Installation (Ubuntu/Debian)

1. **Install Python and Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   ```

2. **Install XAMPP**
   ```bash
   # Download XAMPP Linux Installer
   wget https://www.apachefriends.org/xampp-files/8.1.12/xampp-linux-x64-8.1.12-0-installer.run
   chmod +x xampp-linux-x64-8.1.12-0-installer.run
   sudo ./xampp-linux-x64-8.1.12-0-installer.run
   ```
   - Start MySQL and Apache modules after installation

3. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/chipperhub.git
   cd chipperhub
   ```

4. **Install Python Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

### Running the Application

#### Important: Before Running
- Ensure XAMPP is running
- MySQL service must be active

#### Windows
```bash
python pbl_rks112_kel10.py
```

#### Linux
```bash
python3 pbl_rks112_kel10.py
```

## Automatic Database Creation

The application will automatically:
- Create the required database
- Set up necessary tables
- No manual database configuration needed

## Troubleshooting

- Ensure XAMPP MySQL service is running
- Verify Python dependencies are installed
- Check that all modules are started in XAMPP

## Team Members

- Muhammad Rizqy Nur Faiz (4332401025)
- Devi Natalya (4332401002)
- Gina Thasafiya (4332401003)
- Nursyafika Wahyuni (4332401007)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
