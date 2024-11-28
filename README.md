# Client-Server System for Mathematical Operations

## Project Overview
This project implements a simple client-server system that performs various mathematical operations and commands through socket communication. The system is designed to handle multiple clients simultaneously.

---

## How It Works

### Server Side

1. **User Management (`users`)**  
   - The `users` dictionary is created by the `load_users()` function, which stores usernames and corresponding passwords.  
   - Data is loaded from a file provided as input to the server.

2. **Client Interaction (`stages`)**  
   - The `stages` dictionary tracks the connection state of each client socket:
     - **Stage 0**: User is in the login phase.
     - **Stage 1**: User is logged in and ready to send commands.

3. **Communication Handling (`messages`)**  
   - The `messages` dictionary stores messages to be sent to clients. Messages are updated based on the client's interaction and command execution.

#### Main Server Loop:
- The server uses `select.select()` to monitor multiple sockets, allowing it to handle new connections and incoming data without blocking.
- **New Connections**: When a new client connects, the server accepts the connection.  
- **Login Stage**:  
  - In Stage 0, the server validates the username and password.  
  - Upon successful login, the client transitions to Stage 1, and a welcome message is sent.  
- **Command Handling**:  
  - In Stage 1, the server waits for commands (e.g., `calculate:`, `max:`, `factors:`).  
  - Each command is processed by its corresponding function (e.g., `calculate()`, `find_max()`, `find_prime_factors()`), and the result is sent to the client.  

The server iterates through writable sockets, sending stored messages to each client and removing the socket from the writable list after sending.

---

### Command Processing Functions
- **`calculate(x, y, z)`**: Performs arithmetic operations (addition, subtraction, multiplication, division, exponentiation). Handles overflows and division by zero.  
- **`find_max(numbers)`**: Finds the maximum value in a list of numbers.  
- **`find_prime_factors(n)`**: Returns the prime factors of a given number.

---

### Key Functions
- **`load_users(file_path)`**: Loads user data from a file into a dictionary of valid usernames and passwords.  
- **`handle_login(soc, data, users, stages, messages)`**: Processes login attempts, updates the stage, and sets response messages.  
- **`handle_command(data)`**: Interprets and executes client commands, returning results.

---

### Client-Server Interaction Workflow
1. The server listens for new connections and accepts incoming clients.  
2. Upon connection, the server sends a login prompt.  
3. The client sends login credentials, which are validated by the server. If valid, the server sends a welcome message.  
4. The client sends mathematical commands, which the server processes and returns results.  

---

### Client Side

1. **Key Components**  
   - **`validate_command(command)`**:  
     - Ensures commands follow the correct format and prefix (`calculate:`, `max:`, `factors:`, or `quit`).  
   - **`start_client()`**:  
     - Connects to the server (default: `127.0.0.1:1337`).  
     - Handles login and enters a loop to validate and send commands to the server.  

2. **Command Types**  
   - **`calculate:`**: Requires two integers and an operator.  
   - **`max:`**: Requires a list of integers in parentheses.  
   - **`factors:`**: Expects a number >1 to find its prime factors.  
   - **`quit`**: Terminates the session.  

3. **Error Handling**  
   - **Login Errors**: Invalid credentials prompt a retry or disconnect if the format is incorrect.  
   - **Command Errors**: Invalid command formats display an error and disconnect.  
   - **Connection Issues**: Unreachable server or exceptions display an error and terminate the client.  

---

### Client Flow
1. The client connects to the server and receives a welcome message.  
2. Prompts the user for login credentials and sends them to the server for validation.  
3. Upon successful login, enters a loop for user commands, validates them, sends them to the server, and displays the server’s responses.  
4. Ends the session when the user inputs `quit` or an error occurs.  

---

## Error Handling
- **Login Errors**: Retry on invalid credentials or disconnect on incorrect format.  
- **Command Errors**: Invalid command formats result in an error and disconnect.  
- **Connection Issues**: Displays error messages and terminates the session.
