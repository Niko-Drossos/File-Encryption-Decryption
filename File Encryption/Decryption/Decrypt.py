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

script_directory = os.path.dirname(os.path.dirname(__file__))
folder_path_directory = os.path.join(script_directory, "Decryption", "File Paths")
key_directory = os.path.join(script_directory, "Decryption", "Keys")

def get_key_path(i):
    key_path = os.path.join(key_directory, f"thekey{i}.key")
    return key_path

def decrypt_folder(folder_path, secret_key):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            print(f"Decrypting file: {file_path}")
            # Read the encrypted file contents
            with open(file_path, "rb") as encrypted_file:
                encrypted_contents = encrypted_file.read()

            # Decrypt the contents using the provided key
            decrypted_contents = Fernet(secret_key).decrypt(encrypted_contents)

            # Write the decrypted contents to the file
            with open(file_path, "wb") as decrypted_file:
                decrypted_file.write(decrypted_contents)

def get_last_digits_from_file(file):
    try:
        last_digits = int(''.join(filter(str.isdigit, file)))
        return last_digits
    except ValueError:
        return None
    
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


def main():
    # Import Fernet after ensuring cryptography is installed
    from cryptography.fernet import Fernet

    available_files = get_available_files()

    if not available_files:
        print("No files available for decryption.")
        return

    # Find all the file_path names  and put them in an array "paths"
    paths = []
    for filename in os.listdir(folder_path_directory):
        file_path = os.path.join(folder_path_directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file_contents:
                file_text = file_contents.read()
                paths.append(file_text)


    print("Available files for decryption:")
    print("--------------------------------------------------------------")
    for index, item in enumerate(paths):
        count = index + 1
        print(f"{count}: {item}")
    print("--------------------------------------------------------------")
    choice = input("Enter the number corresponding to the file you want to decrypt (0 to exit): ")
    choice = choice.strip() 
    try:
        choice = int(choice)
    except ValueError:
        input("Invalid input. Please enter a valid number.")
        # main()

    if choice == 0:
        return
    
    file_choice = available_files[choice - 1]
    file_choice_path = os.path.join(folder_path_directory, file_choice)
    i = get_last_digits_from_file(file_choice)
    key_file = get_available_keys(choice)
    key_file_path = os.path.join(key_directory, key_file)
    
    with open(key_file_path, "rb") as key:
        key_contents = key.read()
    with open(file_choice_path, "r") as path:
        file_path = path.read() 

    if not os.path.isdir(file_path):
        print("The file path does not exist, double check the folder has not moved")
        print(file_path)
        main()
        return
    decrypt_folder(file_path, key_contents)
    os.remove(key_file_path)
    os.remove(file_choice_path)
    input("Files decrypted successfully.") 

if __name__ == "__main__":
    main()
