# client.py
import socket
import sys

HEADER = 64  # change this later
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnected."
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    """Encodes message to be sent from client to server."""
    message = msg.encode(FORMAT)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)


def exit_connection():
    """Disconnects from server."""
    send(DISCONNECT_MESSAGE)
    sys.exit(0)


def start():
    """Gets user input to prepare an email to be sent to the server."""
    for i in range(3):
        if i == 0:
            print("Subject of email?")
            msg = input()
            if msg == "!d":
                exit_connection()
            else:
                send(msg)
        elif i == 1:
            print("Who is the recipient?")
            recipient = input()
            if recipient == "!d":
                exit_connection()

            # keeping things simple for demonstration purposes
            while recipient.find("@") == -1:
                print("Not a valid email address. Re-enter recipient.")
                recipient = input()
            send(recipient)
        elif i == 2:
            print("Message body of email?")
            body = input()
            if body == "!d":
                exit_connection()
            else:
                send(body)


while True:
    print("Send a test message! Enter \"!d\" to disconnect from the server at any time.")
    start()
