import os
import importlib.util
import re
import random

script_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_key_path(i):
    # Generate the key file path based on the key number
    key_path = os.path.join(script_directory, "File Encryption", "Decryption", "Keys", f"thekey{i}.key")
    return key_path


def get_file_path(i):
    # Generate the file path for storing the encrypt file path
    file_path = os.path.join(script_directory, "File Encryption", "Decryption", "File Paths", f"EncryptFilePath{i}.txt")
    return file_path


def find_key_files(directory):
    key_files = []
    # Recursively search for key files in the given directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file starts with "thekey" and ends with ".key"
            if file.startswith("thekey") and file.endswith(".key"):
                key_files.append(os.path.join(root, file))
    return key_files


def extract_last_digits(filename):
    # Extract the last digits from the filename
    match = re.search(r"\d+", filename[::-1])
    if match:
        return int(match.group()[::-1])
    return None


# Checks if the folder or any parent directory is already encrypted
def is_folder_encrypted(directory):
    encrypted_paths = []
    encrypt_files_dir = os.path.join(script_directory, "File Encryption", "Decryption", "File Paths")
    encrypt_files = os.listdir(encrypt_files_dir)
    for encrypt_file in encrypt_files:
        file_path = os.path.join(encrypt_files_dir, encrypt_file)
        with open(file_path, "r") as file_contents:
            encrypted_paths.append(file_contents.read())

    # Check if any parent directory of the given directory is already encrypted
    for encrypted_path in encrypted_paths:
        if directory.startswith(encrypted_path):
            return True
    return False


def main():
    # Check if the cryptography module is installed
    try:
        importlib.util.find_spec("cryptography")
        from cryptography.fernet import Fernet
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "cryptography"])
        from cryptography.fernet import Fernet

    try:
        importlib.util.find_spec("tkinter")
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "tkinter"])
        import tkinter as tk
        from tkinter import filedialog

    # Import Fernet after ensuring cryptography is installed
    from cryptography.fernet import Fernet

    # Generate a random number to append to key and file name
    i = random.randint(100000, 999999)
    Key_Path = get_key_path(i)
    File_Path = get_file_path(i)

    # Get the current user's profile directory based on the operating system
    profile_directory = os.path.expanduser("~")

    # Create the main window
    root = tk.Tk()
    root.title("Directory Viewer")

    # Open the file dialog in the current user's profile directory
    directory = filedialog.askdirectory(initialdir=profile_directory, title="Select Directory To Encrypt")
    if not directory:
        root.destroy()
        return
    # Prevent the user from encrypting the script and locking all the previously encrypted files 
    encrypt_protection = os.path.normpath(os.path.normcase(directory).title())
    encrypt_protection = encrypt_protection[0].lower() + encrypt_protection[1:]

    if encrypt_protection == script_directory[0].lower() or encrypt_protection.startswith(script_directory[0].lower()):
        input("Chosen directory is the same as the script directory or its child. You cannot encrypt this software")
        return

    os.chdir(directory)
    print("Selected Folder:", directory)
    root.destroy()  # Close the window after selecting a folder

    # Run a test to check if the folder is already encrypted
    if is_folder_encrypted(directory):
        input("Folder is already encrypted. Press enter to exit...")
        return

    # Function to encrypt the contents of a file
    def encrypt_file(file_path, key):
        try:
            with open(file_path, "rb") as file:
                contents = file.read()
            contents_encrypted = Fernet(key).encrypt(contents)
            with open(file_path, "wb") as file:
                file.write(contents_encrypted)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Failed to encrypt file: {file_path} - {e}")

    # Recursively list all files and folders in the specified folder
    def list_files(start_path, key):
        for root, dirs, files in os.walk(start_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Encrypting file: {file_path}")
                encrypt_file(file_path, key)

    # Function to handle path creation and encryption
    def make_path(directory):
        nonlocal i
        if os.path.isdir(directory):
            key = Fernet.generate_key()

            # Write the encryption key
            with open(Key_Path, "wb") as key_file:
                key_file.write(key)

            # Read the key file
            with open(Key_Path, "rb") as key_file:
                key = key_file.read()

            # Read the path file
            with open(File_Path, "w") as path_file:
                path_file.write(directory)

            list_files(directory, key)
        else:
            print(f"The path '{directory}' is not a directory.")
            input("Try Again")
            make_path(directory)

    # Check if the key file exists and if it does, generate a new "i" value
    if os.path.exists(Key_Path):
        i = random.randint(100000, 999999)
        make_path(directory)
    else:
        make_path(directory)

    # Find key files and extract last digits
    key_files = find_key_files(os.path.dirname(Key_Path))
    for key_file in key_files:
        last_digits = extract_last_digits(key_file)
        if last_digits is not None:
            encrypt_file_path = get_file_path(last_digits)
        else:
            print(f"Failed to extract last digits from: {key_file}")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
