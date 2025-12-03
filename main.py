import secrets
import hashlib
import getpass
import json
import os
import time

# ------------------------------------------------------------
# Load existing users from JSON file (if it exists)
# If the file doesn't exist, create an empty dictionary.
# ------------------------------------------------------------
try:
    with open("users.json", "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

# ------------------------------------------------------------
# Password helper functions
# ------------------------------------------------------------

# Returns True if the entire string contains only lowercase letters
def isAllLowerCase(string):
    for char in string:
        if char.isupper():
            return False
    return True

# Returns True if the string is made only of digits (no letters)
def isAllDigits(string):
    for char in string:
        if char.isalpha():
            return False
    return True

# ------------------------------------------------------------
# Utility: Clears the terminal screen depending on OS
# Windows uses 'cls', Linux/Mac use 'clear'
# ------------------------------------------------------------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------------------------------------------
# Generate a cryptographically secure random salt (in hex)
# Salt protects against rainbow-table attacks
# ------------------------------------------------------------
def generate_salt():
    return secrets.token_hex(16)

# ------------------------------------------------------------
# Hashes the password using SHA-256 with a unique salt
# Adding salt prevents precomputed attacks and makes hashes unique
# ------------------------------------------------------------
def generate_password_hash(password, salt):
    password_hash = (password + salt).encode()
    password_hash = hashlib.sha256(password_hash).hexdigest()
    return password_hash

# ------------------------------------------------------------
# Compare stored hash with a newly generated hash of user input
# ------------------------------------------------------------
def verify(stored_hash, password_try, salt):
    new_hash = generate_password_hash(password_try, salt)
    return stored_hash == new_hash

# Clear the screen at startup
clear()

# ------------------------------------------------------------
# Main application loop
# ------------------------------------------------------------
while True:
    print("1.Register")
    print("2.Login")
    print("3.Exit")
    print("4.Delete User")
    choice = int(input("Chose an option:"))

    # Validate menu choice
    if choice < 1 or choice > 4:
        print("Invalid Choice")
        continue

    # --------------------------------------------------------
    # OPTION 1 — REGISTER NEW USER
    # --------------------------------------------------------
    elif choice == 1:
        clear()
        username = input("Enter Username: ")

        # Prevent duplicate usernames
        if username in users:
            print("Username Already Exists")
            time.sleep(2)
            clear()
            continue

        clear()
        print("Note: The password needs to have:\n")
        print("- at least 8 characters")
        print("- at least one upper-case letter\n")

        # Read password (hidden input)
        password = getpass.getpass("Enter Password: ")

        # Enforce password strength policy
        while len(password) < 8 or isAllLowerCase(password) or isAllDigits(password):
            time.sleep(1)
            clear()

            if len(password) < 8:
                password = getpass.getpass("The Password is too short, try again:")
            elif isAllLowerCase(password):
                password = getpass.getpass("The Password has no upper-case letters, try again:")
            elif isAllDigits(password):
                password = getpass.getpass("The Password only contains numbers, try again:")

        clear()

        # Create salt + hashed password
        salt = generate_salt()
        password_hash = generate_password_hash(password, salt)

        # Ask user to verify the password
        verification = getpass.getpass("Verify Password: ")
        attempts = 0

        while not verify(password_hash, verification, salt) and attempts < 3:
            time.sleep(1)
            clear()
            verification = getpass.getpass("Try again: ")
            attempts += 1

        if attempts == 3:
            time.sleep(2)
            clear()
            continue

        # Store new user into dictionary
        users[username] = {"hash": password_hash, "salt": salt}

        # Write updated users dictionary to JSON
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

        print("Registration Successful!")
        time.sleep(1)
        clear()

    # --------------------------------------------------------
    # OPTION 2 — LOGIN
    # --------------------------------------------------------
    elif choice == 2:
        clear()
        username = input("Enter Username: ")

        if username not in users:
            print("You are not registered!")
            time.sleep(2)
            clear()
            continue

        clear()
        password = getpass.getpass("Enter Password: ")
        salt = users[username]["salt"]
        password_hash = generate_password_hash(password, salt)

        # Compare the stored hash with user input hash
        if users[username]["hash"] == password_hash:
            print("Password Match!")
            time.sleep(2)
            clear()
        else:
            print("Password did not Match!")
            time.sleep(2)
            clear()

    # --------------------------------------------------------
    # OPTION 3 — EXIT PROGRAM
    # --------------------------------------------------------
    elif choice == 3:
        exit()

    # --------------------------------------------------------
    # OPTION 4 — DELETE USER
    # --------------------------------------------------------
    elif choice == 4:
        clear()
        username = input("Enter the user you want to delete:")

        if username not in users:
            print("The user does not exist!")
            time.sleep(2)
            clear()
            continue

        confirm = input("Are you sure you want to delete this user? (y/n): ").lower()
        clear()

        if confirm != 'y':
            print("Deletion Canceled!")
            time.sleep(1)
            clear()
            continue

        # Require password to confirm deletion
        password_try = getpass.getpass("Please enter the user's password to continue: ")
        deletion_hash = generate_password_hash(password_try, users[username]["salt"])

        if deletion_hash == users[username]["hash"]:
            del users[username]

            # Save the updated JSON file after deletion
            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)

            print("User Deleted!")
            time.sleep(1)
            clear()
        else:
            print("Password not matched!")
            time.sleep(2)
            clear()
