@echo off
echo E: Encrypt Folder
echo D: Decrypt Folder
choice /c ED /n /m "Enter your choice: "

if errorlevel 2 (
    echo Running Decrypt
    start "Decrypt Files" ".\File Encryption\Decryption\Decrypt.py"
) else (
    echo Running Encrypt
    start "Encrypt Files" ".\File Encryption\Encryption\Encrypt.py"
)
