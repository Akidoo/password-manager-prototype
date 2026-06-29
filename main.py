import sys
import json
from cryptography.fernet import Fernet
from pathlib import Path

def main():
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
                password = input("Password: ")
                key = Fernet.generate_key()
                f = Fernet(key)
                encrypted_password = f.encrypt(password)
                current1 = fileOpener()
                current1[service] = {"username": username, "password": encrypted_password.decode(), "key": key.decode()}
                fileSaver(current1)
                print(f"Details for {service} added successfully!")
            elif choice == 2:
                current2 = fileOpener()
                print(current2)
                break
            elif choice == 3:
                search = input("Search accounts: ")
                current3 = fileOpener()
                if search in current3:
                    print(f"Details for {search}:")
                    print(f"Username: {current3[search]['username']}")
                    print(f"Password: {current3[search]['password']}")
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