# Important Notice

**The user of this software assumes ALL LIABILITY for lost or corrupted files.**

## Installation

Before you use the script, you will need to install Python on the host machine, just click on `Download Python.bat` and it will take you to the python download page. 
The first time you run `Encrypt.py`, it will start installing `cryptography.Fernet` and `tkinter`. Just run the script a second time after it finishes installing for it to work.

## !!WARNING!!

- **DO NOT LOSE THE KEYS:** If you lose the keys to the encryption, you WILL LOSE THE FILES.
- **DO NOT CHANGE FOLDER PATHS OF ENCRYPTED FILES:** This script works by saving the path of the selected folder, so if you change the path, the script won't be able to find the folder.
- **Do not change the files paths within the app.**
- **Before updating your local script make sure you have no encrypted files** You will lose your keys and the files or the Decrypt script may not be compatible with a previous version.

## Recommended Use Case

- Have the script on a USB drive so you can keep the keys somewhere safe.
- Alternatively, you can start the `startApp.bat`, a shortcut on the desktop, and keep the software on your computer.
- Try to keep encryptions relatively small to minimize the chance of failure.
- Make sure to have a backup when you encrypt files.

## Encrypting Files

To encrypt files, follow these steps:

1. Start `startApp.bat`.
2. Press "E" to start `Encrypt.py`.
3. Select a folder from the file explorer, and the files inside the folder will start encrypting.
   - This process only encrypts files inside folders so you must select a folder; it will iterate over all files and directories inside the selected folder.
4. Once encryption is complete, the script will list all the files that have been encrypted.

## Decrypting Files

To decrypt files, follow these steps:

1. Start `startApp.bat`.
2. Press "D" to start `Decrypt.py`.
3. A CMD prompt will pop up, asking you to input the corresponding number to the folder you decrypted.
4. The script will list all the files that have been decrypted.
5. Press Enter, and you're done!

## Credits and Contact Information

Program designed by Niko Drossos 

[Git-Hub](https://github.com/Niko-Drossos)
[ALT Git-Hub](https://github.com/AvarageCodeEnjoyer)

If you have any ideas or suggestions, please feel free to reach out to me!

## Liability 

By using this open sorce software, you assume all liabilities. I am not responsible for the loss or corruption of files.
