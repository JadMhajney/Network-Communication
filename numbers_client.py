#!/usr/bin/python3
from socket import *
import sys


def validate_command(command):
    try:
        # Command must start with a valid prefix
        if command.startswith("calculate: "):
            parts = command[len("calculate: "):].split()
            if len(parts) != 3:
                return False
            x, z, y = parts
            if not (x.lstrip("-").isdigit() and y.lstrip("-").isdigit()):
                return False
            if z not in ["+", "-", "*", "/", "^"]:
                return False
            return True

        elif command.startswith("max: "):
            args=command[len("max: "):]
            if not (args.startswith("(") and args.endswith(")")):
                return False
            numbers = args.strip("()").split()
            if not all(num.lstrip("-").isdigit() for num in numbers):
                return False
            return True

        elif command.startswith("factors: "):
            number = command[len("factors: "):].strip()
            if not number.isdigit():  # Check if it's not a number string
                return False
            if int(number) <= 1:  # Check if the number is less than 1
                return False
            return True

        elif command.strip() == "quit":
            return True

        else:
            return False
    except Exception:
        return False
    

def start_client():
    # Default host and port
    host = '127.0.0.1'
    port = 1337

    # Parse command-line arguments
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    elif len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            print_error("Invalid input. Port requires hostname.")
            return
        else:
            host = sys.argv[1]

    try:
        # Create and connect the socket
        with socket(AF_INET, SOCK_STREAM) as clientSoc:
            clientSoc.connect((host, port))
            print(clientSoc.recv(1024).decode())  # Welcome message

            # Login loop
            while True:
                user_name = input()
                if not user_name.startswith("User: "):
                    print_error("Failed to login.")
                    return
                    #continue

                password = input()
                if not password.startswith("Password: "):
                    print_error("Failed to login..")
                    return
                    #continue

                # Send credentials to server
                data = f"{user_name.split(': ')[1]} {password.split(': ')[1]}"
                clientSoc.send(data.encode())

                # Receive server response
                msg = clientSoc.recv(1024).decode()
                print(msg)
                if msg == "Failed to login":
                    continue
                elif "good to see you" in msg:
                    break

            # Command loop
            while True:
                func = input()
                if not validate_command(func):
                    print_error("Invalid command format. Disconnecting.")
                    break  # Disconnect from the server
                
                clientSoc.send(func.encode())
                response = clientSoc.recv(1024).decode()
                if response == "quit":
                    print("Disconnected from server.")
                    return
                print(response)

    except Exception as e:
        print_error(f"An error occurred: {e}")


def print_error(message):
    print(f"Error: {message}")


if __name__ == '__main__':
    start_client()
