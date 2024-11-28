Communication Networks- 0368303001 HW1
Maya Khuri 212719124  Jad Mahajne 318978152
Project Overview
The project implements a simple client-server system that performs various mathematical operations and commands through socket communication. The system is designed to handle multiple clients simultaneously .

How It Works
Server Side:
1.	User Management (users)
The users dictionary is created by the load_users function, which stores usernames and their corresponding passwords. The data is loaded from a file provided as input to the server.
2.	Client Interaction (stages)
The stages dictionary keeps track of the connection state of each client socket. The stages are represented by numbers:
o	Stage 0: User is in the login phase.
o	Stage 1: User is logged in and ready to send commands.
3.	Communication Handling (messages)
The messages dictionary stores messages to be sent to clients. These messages are updated based on the client's interaction and command execution.
Main Server Loop:
The server continuously loops, using the select.select() method to monitor multiple sockets. This allows it to handle both new connections and incoming data from clients without blocking. It listens for new connections and incoming data from clients:
•	New Connections: When the listening socket appears in the readable list, it indicates that a new client is attempting to connect. The server then accepts the connection 
•	Login Stage: If a client is in stage 0 (login phase), the server validates the username and password. Upon successful login, the stage is updated to 1 and a welcome message is sent.
•	Command Handling: When the client is logged in (stage 1), the server waits for commands (e.g., calculate:, max:, factors:). Each command is processed by the corresponding function (e.g., calculate(), find_max(), find_prime_factors()), and the result is sent back to the client.
The server iterates through the writable sockets and sends the stored messages to each client. After sending the message, the socket is removed from the writable list.
Command Processing Functions:
•	calculate(x, y, z): Performs arithmetic operations (addition, subtraction, multiplication, division, exponentiation) and checks for overflows or division by zero.
•	find_max(numbers): Finds the maximum value from a list of numbers.
•	find_prime_factors(n): Returns the prime factors of a given number.
Client-Server Interaction Workflow:
1.	The server listens for new connections and accepts incoming clients.
2.	Upon a new connection, the server sends a login prompt.
3.	The client sends the login credentials (username and password). If valid, the server responds with a welcome message and transitions to the command phase.
4.	The client sends mathematical commands, which the server processes and returns results.
Key Functions and Handling:
•	load_users(file_path): Loads user data from the provided file, creating a dictionary of valid usernames and passwords.
•	handle_login(soc, data, users, stages, messages): Processes the login attempt and updates the stage and message based on the result.
•	handle_command(data): Interprets and processes the client's command, executing the appropriate operation and returning the result.
Client-Side
Key Components:
1.	validate_command(command):
o	Validates the format of the user's input command.
o	Ensures that the command starts with the correct prefix (e.g., calculate:, max:, factors:, or quit).
o	Checks the correctness of arguments within each command.
2.	start_client():
o	Initiates the client by connecting to the server at a specified host and port (default: 127.0.0.1:1337).
o	Handles the login process by sending the username and password to the server, checking the response, and prompting the user to retry on failed login.
o	Once logged in, the client enters a command loop where it validates and sends commands to the server for execution, then displays the server's response.
o	Supports command types: calculate:, max:, factors:, and quit.
3.	Command Validation:
o	calculate: command requires three arguments (two integers and an operator).
o	max: command requires a list of integers inside parentheses.
o	factors: command expects a number greater than 1 to find its prime factors.
o	quit terminates the client session.
4.	Error Handling:
o	If a command is invalid or incorrectly formatted, the client displays an error message and disconnects.
5.	User Interaction:
o	Prompts the user for login credentials (username and password).
o	Prompts the user for commands after login and displays the result or error message from the server.
Client Flow:
1.	The client connects to the server and displays a welcome message.
2.	It prompts the user for login credentials, validates the input, and sends the credentials to the server.
3.	After a successful login, the client enters a loop where the user can input commands. Each command is validated and sent to the server.
4.	The server’s response is displayed, and the loop continues until the user inputs quit or an error occurs.
Error Handling:
•	Login Errors: If the login credentials are invalid, the client will show an error message and prompt the user to retry. And if the format is incorrect  then disconnect.
•	Command Errors: If the user inputs an invalid command format, the client will display an error and disconnect.
•	Connection Issues: If the server is unreachable or an exception occurs, the client will display an error message and terminate.

