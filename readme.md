# Chipperhub - Substitution Cipher Application
![Python Logo](https://www.python.org/static/community_logos/python-logo.png) ![Politeknik Negeri Batam Logo](https://dianisa.com/wp-content/uploads/2020/06/logo-politeknik-negeri-batam.png)

## Project Overview

Chipperhub is a comprehensive desktop application developed for educational purposes, providing a secure and user-friendly platform for text encryption, decryption, and network security tools.

## Features

- 🔐 Secure User Authentication System
- 🔒 Password Hashing with BCrypt
- 🔤 Substitution Cipher Encryption/Decryption
- 📋 Clipboard Integration (Copy/Paste Functionality)
- 🖥️ Intuitive Tkinter-based User Interface
- 🎥 Video Playback Support (Welcome Screen)
- 🌐 Network Security Tools:
  - Ping to Get IP Address
  - Port Scanning
  - Vulnerability Scanning with Nmap and Bandit
- 🔧 Crypto Tools:
  - Binary Text Converter
  - Morse Code Converter
  - Alphabet Phonetic Converter

## System Requirements

### Hardware Requirements
- Processor: 1 GHz or faster
- RAM: Minimum 2 GB
- Disk Space: 100 MB free space

### Software Requirements
- Python 3.8 or higher
- MySQL Server or XAMPP
- Nmap
- Git (optional, for cloning repository)

## Installation Guide

### Preparation

#### Windows Installation

1. **Install Python**
   - Download Python from [Official Python Website](https://www.python.org/downloads/).
   - During installation, check "Add Python to PATH."
   - Verify installation by opening Command Prompt and running:
     ```bash
     python --version
     pip --version
     ```

2. **Install XAMPP**
   - Download XAMPP from [Apache Friends](https://www.apachefriends.org/).
   - Install XAMPP.
   - Start Apache and MySQL modules from XAMPP Control Panel.

3. **Clone the Repository**
   ```bash
   git clone https://github.com/paizy-hub/chipperhub.git
   cd chipperhub
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install python-nmap
   ```

#### Linux Installation (Ubuntu/Debian)

**Option 1: Install with XAMPP**
1. **Install Python and Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk nmap
   ```

2. **Install XAMPP**
   ```bash
   # Download XAMPP Linux Installer
   wget https://www.apachefriends.org/xampp-files/8.1.12/xampp-linux-x64-8.1.12-0-installer.run
   chmod +x xampp-linux-x64-8.1.12-0-installer.run
   sudo ./xampp-linux-x64-8.1.12-0-installer.run
   ```
   - Start MySQL and Apache modules after installation.

**Option 2: Install with MySQL Server**
1. **Install Python, MySQL, and Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk mysql-server nmap
   ```

2. **Start MySQL Service**
   ```bash
   sudo systemctl start mysql
   sudo systemctl enable mysql
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/paizy-hub/chipperhub.git
   cd chipperhub
   ```

4. **Install Python Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

### Running the Application

#### Windows
```bash
python chipperhub.py
```

#### Linux
```bash
python3 chipperhub.py
```

## Troubleshooting

- Ensure MySQL service is running.
- Verify Python dependencies are installed.
- Confirm Nmap is correctly installed.
- Check database connection settings.
- Ensure all required modules are installed.

## Team Members

- Muhammad Rizqy Nur Faiz (4332401025)
- Devi Natalya (4332401002)
- Gina Thasafiya (4332401003)
- Nursyafika Wahyuni (4332401007)

## Contributing

1. Fork the repository.
2. Create your feature branch.
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.
