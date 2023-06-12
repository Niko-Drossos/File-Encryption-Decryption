import os
import re
import random
import subprocess

# ------------------------------- Path Creation ------------------------------ #

# Create dir "Keys" & "File Paths" if they do not already exist 
def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

script_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Define key folder location
key_files = os.path.join(script_directory, "File Encryption", "Decryption", "Keys")
create_directory_if_not_exists(key_files)

# Define file path folder location
path_files = os.path.join(script_directory, "File Encryption", "Decryption", "File Paths")
create_directory_if_not_exists(path_files)

# Generate the key file name based on the random number
def get_key_path(random_number):
    key_path = os.path.join(key_files, f"theKey{random_number}.key")
    return key_path

# Generate the file name for storing the encrypt file path
def get_file_path(random_number):
    file_path = os.path.join(path_files, f"EncryptFilePath{random_number}.txt")
    return file_path

# -------------------------- Tests Before Encryption ------------------------- #

# Ask the user to confirm if it is the correct folder they want encrypted
def confirm_choice(directory):
    confirm = input(f'Confirm "{directory}" is folder you want encrypted: (y / n): ')
    if confirm == "n":
        print("Stopping")
        return False
    elif confirm == "y":
        print("Selected Folder:", directory)
        return True
    else:
        print("Invalid input try again")
        return confirm_choice(directory)

# Extract the last digits from the filename
def extract_last_digits(filename):
    # Uses regex to find all the numbers at the end of the filename string
    match = re.search(r"\d+", filename[::-1])
    if match:
        return int(match.group()[::-1])
    return None


# Checks if the folder or any parent directory is already encrypted
def is_folder_encrypted(directory):
    """
    Check if the specified folder or any of its parent directories is already encrypted.

    Args:
        directory (str): The path to the directory to be checked for encryption.

    Returns:
        bool: True if the directory or any parent directory is already encrypted, False otherwise.
    """
    encrypted_paths = []
    encrypt_files = os.listdir(path_files)
    for encrypt_file in encrypt_files:
        file_path = os.path.join(path_files, encrypt_file)
        with open(file_path, "r") as file_contents:
            encrypted_paths.append(file_contents.read())

    # Check if any parent or child directory of the given directory is already encrypted
    for encrypted_path in encrypted_paths:
        if directory.startswith(encrypted_path):
            return True
        elif encrypted_path.startswith(directory):
            return True
    return False

# -------------------------------- Find Files -------------------------------- #

# Find all the key files inside of the "Keys" directory
def find_key_files():
    """
    Find all key files inside the specified keys_folder directory.

    Args:
        keys_folder (str): The path to the directory containing the key files.

    Returns:
        List[str]: A list of paths to the key files found in the keys_folder directory,
                   matching the naming convention "theKey*.key".
    """
    keys = []
    for root, dirs, files in os.walk(key_files):
        for file in files:
            # Check if the file starts with "theKey" and ends with ".key"
            if file.startswith("theKey") and file.endswith(".key"):
                keys.append(os.path.join(root, file))
    return keys

# ---------------------------------------------------------------------------- #


def main():
    # Check if the cryptography module is installed
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        subprocess.run(["pip", "install", "cryptography"])
        from cryptography.fernet import Fernet

    # Check if tKinter is already installed
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        subprocess.run(["pip", "install", "tkinter"])
        import tkinter as tk
        from tkinter import filedialog

    # Generate a random number to append to key and file name to pair them up
    random_number = random.randint(100000, 999999)
    Key_Path = get_key_path(random_number)
    File_Path = get_file_path(random_number)

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
    
    # Make the directory path look cleaner 
    directory = os.path.normpath(directory)

    # Make sure they want to encrypt that folder, if not then return
    if not confirm_choice(directory):
        return

    # Prevent the user from encrypting the script and locking all the previously encrypted files 
    cant_encrypt = os.path.normcase(directory).title()
    encrypt_protection = cant_encrypt[0].lower() + cant_encrypt[1:]

    # Prevents you from encrypting the script file or any of its children
    if encrypt_protection.lower() == script_directory.lower() or encrypt_protection.lower().startswith(script_directory.lower()):
        print(f"Path not able to be encrypted: {script_directory.lower()}")
        print(f"Path being encrypted: {encrypt_protection.lower()}")
        input("Chosen directory is the same as the script directory or its child. You cannot encrypt this software")
        return

    # Change directory to selected one and print it to the stdout
    os.chdir(directory)
    root.destroy()  # Close the window after selecting a folder

    # Run a test to check if the folder is already encrypted
    if is_folder_encrypted(directory):
        input(f'Folder "{directory}" already contains encrypted files. \nPress enter to exit...')
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
        nonlocal random_number
        if os.path.isdir(directory):
            key = Fernet.generate_key()

            # Write the encryption key
            with open(Key_Path, "wb") as key_file:
                key_file.write(key)

            # Read the path file
            with open(File_Path, "w") as path_file:
                path_file.write(directory)

            list_files(directory, key)
        else:
            print(f"The path '{directory}' is not a directory.")
            input("Try Again")
            main()

    # Check if the key file exists and if it does, generate a new "random_number" value
    if os.path.exists(Key_Path):
        random_number = random.randint(100000, 999999)
        make_path(directory)
    else:
        make_path(directory)

    # Find key files and extract last digits
    key_files = find_key_files()
    for key_file in key_files:
        last_digits = extract_last_digits(key_file)
        if last_digits is not None:
            encrypt_file_path = get_file_path(last_digits)
        else:
            print(f"Failed to extract last digits from: {key_file}")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()