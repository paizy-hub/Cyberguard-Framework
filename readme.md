# CYBERGUARD-FRAMEWORKS
<img src="https://github.com/paizy-hub/chipperhub/blob/main/logopoltek.png" alt="Politeknik Negeri Batam Logo" width="200"/> <img src="https://github.com/paizy-hub/chipperhub/blob/main/logorks.png" alt="RK Logo" width="200"/>

## Project Overview

Cyberguard Frameworks is a comprehensive desktop application developed for educational purposes, providing a secure and user-friendly platform for text encryption, decryption, and network security tools.

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
- Python 3.12
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
   git clone https://github.com/paizy-hub/Cyberguard-Frameworks.git
   cd Cyberguard-Frameworks
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

#### Linux Installation (Arch Linux)

**Option 1: Install with XAMPP**
1. **Install Python and Dependencies**
   ```bash
   sudo pacman -Syu
   sudo pacman -S python python-pip tk nmap
   ```

2. **Install XAMPP**
   ```bash
   # Download XAMPP Linux Installer
   wget https://www.apachefriends.org/xampp-files/8.1.12/xampp-linux-x64-8.1.12-0-installer.run
   chmod +x xampp-linux-x64-8.1.12-0-installer.run
   sudo ./xampp-linux-x64-8.1.12-0-installer.run
   ```
   - Start XAMPP services:
   ```bash
   sudo /opt/lampp/lampp start
   ```

**Option 2: Install with MariaDB (MySQL)**
1. **Install Python, MariaDB, and Dependencies**
   ```bash
   sudo pacman -Syu
   sudo pacman -S python python-pip tk mariadb nmap
   ```

2. **Initialize and Start MariaDB**
   ```bash
   sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   ```

3. **Secure MariaDB Installation**
   ```bash
   sudo mysql_secure_installation
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/paizy-hub/Cyberguard-Frameworks.git
   cd Cyberguard-Frameworks
   ```

4. **Install Python Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

### Running the Application

#### Windows
```bash
python Cyberguard-Frameworks.py
```

#### Linux
```bash
python3 Cyberguard-Frameworks.py
```

## Troubleshooting

- Ensure MySQL service is running.
- Verify Python version and dependencies are installed.
- Confirm Nmap is correctly installed.
- Check database connection settings.
- Ensure all required modules are installed.
- For Arch Linux users: If using MariaDB, ensure it's properly configured and running before starting the application.

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
