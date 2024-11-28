#!/usr/bin/python3
import socket
import select
import sys
from socket import *

def calculate(x, y, z):
    INT32_MIN = -2_147_483_648
    INT32_MAX = 2_147_483_647
    x = int(x)
    y = int(y)
    if z == "+":
        res = x + y
    elif z == "-":
        res = x - y
    elif z == "*":
        res = x * y
    elif z == "/":
        if y == 0:
            return "error: division by zero"
        res = round(x / y, 2)
    elif z == "^":
        res = x ** y
    else:
        return "error: invalid operator"

    if res < INT32_MIN or res > INT32_MAX:
        return "error: result is too big"
    return str(res)

def find_max(numbers):
    numbers = [int(num) for num in numbers]
    return max(numbers)

def find_prime_factors(n):
    n = int(n)
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    divisor = 3
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.add(divisor)
            n //= divisor
        divisor += 2
    if n > 2:
        factors.add(n)
    return list(factors)

def start_server():
    port = 1337
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
    users = load_users(sys.argv[1])

    clients = {}
    stages = {}

    # Create the listening socket
    with socket(AF_INET, SOCK_STREAM) as listeningSocket:
        listeningSocket.bind(('', port))
        listeningSocket.listen(len(users))
        print(f"Server is listening on port {port}...")

        # Use select to handle multiple clients
        rlist = [listeningSocket]
        wlist = []
        messages = {}

        while True:
            readable, writable, _ = select.select(rlist, wlist, [])
            for soc in readable:
                if soc is listeningSocket:
                    conn, addr = listeningSocket.accept()
                    print(f"New connection from {addr}")
                    rlist.append(conn)
                    stages[conn] = 0  # Initial stage: not logged in
                    messages[conn] = "Welcome! Please log in."
                    wlist.append(conn)
                else:
                    try:
                        data = soc.recv(1024).decode()
                        if not data: #if no data was recieved from the client disconnect him
                            disconnect_client(soc, rlist, wlist, stages, messages)
                            continue
                        if stages[soc] == 0:  # Login stage
                            handle_login(soc, data, users, stages, messages)
                            wlist.append(soc) 
                        else:  # Command handling stage - stage 1
                            response = handle_command(data)
                            messages[soc] = response
                            wlist.append(soc)

                    except Exception as e:
                        print(f"Error with client {soc.getpeername()}: {e}")
                        disconnect_client(soc, rlist, wlist, stages, messages)

            for soc in writable:
                if soc in messages:
                    soc.send(messages[soc].encode())
                    messages.pop(soc)
                    wlist.remove(soc)

def load_users(file_path):
    users_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            username, password = line.strip().split("\t")
            users_dict[username] = password
    return users_dict

def handle_login(soc, data, users, stages, messages):
    try:
        username, password = data.split(" ") #the data is recieved in the format : "{username} {password}""
        if username in users and users[username] == password:
            stages[soc] = 1  # Logged in
            messages[soc] = f"Hi {username}, good to see you."
            return True
        else:
            messages[soc] = "Failed to login."
            return False
    except ValueError:
        messages[soc] = "Failed to login."
        return False

def handle_command(data):
    try:
        if data.startswith("calculate:"):
            operation = data[len("calculate:") + 1 :]
            x, z, y = operation.split()
            res = calculate(x, y, z)
            if(res.startswith("error: ")):
                return res
            return f"response: {res}"

        elif data.startswith("max:"):
            numbers = data[len("max:") + 1 :]
            numbers = numbers.strip("()").split()
            return f"the maximum is {find_max(numbers)}"

        elif data.startswith("factors:"):
            number = data.split(": ")[-1]
            factors = find_prime_factors(int(number))
            return f"the prime factors of {number} are: {', '.join(map(str, factors))}"

        elif data.strip() == "quit":
            return "quit"

        else:
            return "error: unknown command"
    except Exception as e:
        return f"error: {e}"

def disconnect_client(soc, rlist, wlist, stages, messages):
    print(f"Client {soc.getpeername()} disconnected.")
    if soc in rlist:
        rlist.remove(soc)
    if soc in wlist:
        wlist.remove(soc)
    if soc in stages:
        del stages[soc]
    if soc in messages:
        del messages[soc]
    soc.close()

if __name__ == '__main__':
    start_server()
