# server.py
import socket
import threading
import os
import smtplib
import json
from email.message import EmailMessage
from pathlib import Path

# import functions database.py and rsa.py
from database import *
from rsa import *

# Socket stuff
HEADER = 64  # change this later
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Disconnected."

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

cwd = Path(__file__).parents[0]
cwd = str(cwd)

# Email credentials
# This uses the environment variables that I have set on my personal PC.
# It will not work on other computers.
# EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
# EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

# This will be the email address that sends the test emails from this application.
# Use this instead if trying to replicate on a different computer.
EMAIL_ADDRESS = json.load(open(cwd + '/credentials/address.json'))['address']
EMAIL_PASSWORD = json.load(open(cwd + '/credentials/password.json'))['password']


def handle_smtp(email):
    """Handles the sending of emails"""
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # SMTP_SSL is a function that establishes an SSL encrypted connection
        # This encrypts the traffic when the emails are being sent.
        # SSL encryption is an asymmetric encryption algorithm.
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(email)


def handle_database(email_msg):
    """Handles the encryption/decryption and storing of emails"""
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    # Encrypting data here
    private_key = import_key("private_key.pem")
    public_key = get_public_key(private_key)
    message_of_email = email_msg[2].encode('ascii')
    encrypted_message = encrypt(public_key, message_of_email)

    insert_element(EMAIL_ADDRESS, email_msg[1], email_msg[0], encrypted_message, cur, conn)

    # Decrypting data here
    row_number = get_number_of_rows(cur)
    record = get_row_from_id(row_number, cur)
    decrypted_message = decrypt(private_key, record[4])
    decrypted_message = decrypted_message.decode('ascii')

    # Prepare email to send via SMTP
    email_to_send = EmailMessage()
    email_to_send['Subject'] = email_msg[0]
    email_to_send['From'] = EMAIL_ADDRESS
    email_to_send['To'] = email_msg[1]
    email_to_send.set_content(decrypted_message)

    return email_to_send


def handle_client(conn, addr):
    """Handles the client which sends over user input."""
    print(f"{addr} connected.")
    email_msg = []
    count = 0
    connected = True

    while connected:
        if count > 2:
            email_msg = []
            count = 0
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] {msg}")
                continue
            else:
                email_msg.append(msg)
                count += 1

                # if all required information is in the list
                if count == 3:
                    email_to_send = handle_database(email_msg)

                    handle_smtp(email_to_send)
                    print("Message received.")

    conn.close()


def start():
    """Start the server"""
    server.listen()
    print("Server is listening on " + SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"Active connections: {threading.activeCount() - 1}")


if __name__ == "__main__":
    print("Server is starting...")
    start()
