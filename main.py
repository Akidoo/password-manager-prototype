import sys
import json
from cryptography.fernet import Fernet
from pathlib import Path
import secrets
import hashlib
import tkinter as tk


def main():
    root = tk.Tk()
    root.title("pVault")
    root.geometry("400x550")
    file_path = Path("passwords.json")
    passwordEntry = tk.Entry(root, show="*")
    passwordEntry.pack(pady=10)

    submitButton = tk.Button(root, text="Submit")
    submitButton.pack(pady=10)

    if not file_path.exists():
        salt = secrets.token_bytes(16)
        masterPassword = input("Set a master password: ").encode()
        masterPasswordHash = hashlib.pbkdf2_hmac('sha256', masterPassword, salt, 100000)
        config = {
            "config": {
                "salt": salt.hex(),
                "masterPasswordHash": masterPasswordHash.hex()
            },
            "vault" : {}
        }
        fileSaver(config)
    else:
        masterPassword = input("Enter the master password: ").encode()
        with open("passwords.json", "r") as file:
            data = json.load(file)
        salt = bytes.fromhex(data["config"]["salt"])
        masterPasswordHash = hashlib.pbkdf2_hmac('sha256', masterPassword, salt, 100000)
        if masterPasswordHash.hex() != data["config"]["masterPasswordHash"]:
            print("Incorrect master password.")
            sys.exit(1)

    while True:
        print("1. Add a new item")
        print("2. View all items")
        print("3. Search details")
        print("4. Exit")
        try:
            choice = int(input("Select an option: "))

            if choice == 1:
                service = input("Service: ")
                username = input("Username: ")
                password = input("Password: ").encode()
                key = Fernet.generate_key()
                f = Fernet(key)
                encrypted_password = f.encrypt(password)
                current1 = fileOpener()
                current1["vault"][service] = {"username": username, "password": encrypted_password.decode(), "key": key.decode()}
                fileSaver(current1)
                print(f"Details for {service} added successfully!")
            elif choice == 2:
                current2 = fileOpener()
                account_list = current2["vault"]
                print(account_list)
                break
            elif choice == 3:
                search = input("Search accounts: ")
                current3 = fileOpener()
                if search in current3["vault"]:
                    print(f"Details for {search}:")
                    print(f"Username: {current3['vault'][search]['username']}")
                    print(f"Password: {current3['vault'][search]['password']}")
                else:
                    print(f"No details found for {search}.")
            elif choice == 4:
                print("Exiting the program.")
                sys.exit(0)
            else:
                print()
                print("Invalid option. Please try again.")
                print()
        except ValueError:
            print("An error occurred. Please enter a valid number.")
            sys.exit(1)

def fileOpener():
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found. Creating a new file.")
        data = {}
    return data

def fileSaver(data):
    with open("passwords.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()