import os
import importlib.util

# Check if the cryptography module is installed
try:
    importlib.util.find_spec("cryptography")
    from cryptography.fernet import Fernet
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "cryptography"])
    from cryptography.fernet import Fernet

# ------------------------------- Path Creation ------------------------------ #

# Set paths for the script file, key and path files
script_directory = os.path.dirname(os.path.dirname(__file__))
folder_path_directory = os.path.join(script_directory, "Decryption", "File Paths")
key_directory = os.path.join(script_directory, "Decryption", "Keys")

# --------------------------- Select File From List -------------------------- #

# Ask for input on file to decrypt
def select_path(count):
    choice = input("Enter the number corresponding to the file you want to decrypt (0 to exit): ")
    choice = choice.strip() 
    try:
        choice = int(choice)
        if choice == 0: 
            return False
        # if number input is larger then the number of files available for decryption then ask for input again
        elif choice > count:
            print(f"Number {choice} not on list")
            return select_path(count)
        return choice
    # If input is not a number throw an error
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return select_path(count)
    
# get all file paths in File Paths folder 
def get_available_files():
    available_files = []
    for file_path in os.listdir(folder_path_directory):
        available_files.append(file_path)
    # available_files.sort()
    return available_files

# Get all keys in Keys folder
def get_available_keys(i):
    keys = []
    for key_file in os.listdir(key_directory):
        keys.append(key_file)
    return keys[i - 1] 

# ------------------------------- Decrypt Files ------------------------------ #

def decrypt_folder(folder_path, secret_key):
    failed = False
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Read the encrypted file contents
            with open(file_path, "rb") as encrypted_file:
                encrypted_contents = encrypted_file.read()

            # Decrypt the contents using the provided key
            try:
                decrypted_contents = Fernet(secret_key).decrypt(encrypted_contents)
                print(f"Decrypting file: {file_path}")
                # Write the decrypted contents to the file
                with open(file_path, "wb") as decrypted_file:
                    decrypted_file.write(decrypted_contents)
            except:
                print(f"Failed to decrypt {file_path}")
                failed = True
    return failed
    
# ---------------------------------------------------------------------------- #

def main():
    # Make a list of all available files for decryption 
    available_files = get_available_files()

    # Return early if there ar no files in "File Paths"
    if not available_files:
        input("No files available for decryption. Press Enter to exit...")
        return

    # Find all the file_path names  and put them in an array "paths"
    paths = []
    for filename in os.listdir(folder_path_directory):
        file_path = os.path.join(folder_path_directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file_contents:
                paths.append(file_contents.read())

    # List all files available for decryption
    count = 0
    print("Available files for decryption:")
    print("--------------------------------------------------------------")
    for index, item in enumerate(paths):
        count += 1
        print(f"{index + 1}: {item}")
    print("--------------------------------------------------------------")

    choice = select_path(count)
    if not choice:
        return

    file_choice = available_files[choice - 1]
    file_choice_path = os.path.join(folder_path_directory, file_choice)

    key_file = get_available_keys(choice)
    key_file_path = os.path.join(key_directory, key_file)
    
    with open(key_file_path, "rb") as key:
        key_contents = key.read()
    with open(file_choice_path, "r") as path:
        file_path = path.read() 

    if not os.path.isdir(file_path):
        print(f'The file path "{file_path}" does not exist, \ndouble check the folder has not moved')
        main()
        return
    
    if decrypt_folder(file_path, key_contents):
        return
    # Remove key and file path files after decryption
    os.remove(key_file_path)
    os.remove(file_choice_path)
    input("Files decrypted successfully.") 

# Invoke the main function
if __name__ == "__main__":
    main()
