# IFT 520 Final Project
Auto-encrypts an email's message body and stores this in a local database. The email is then sent to the specified recipient email address.

### Components developed are as follows: <br/>
Client and Server (Socket Programming) <br/>
Database (SQLite3) <br/>
RSA Encryption <br/>

### How it all works:
1) Run the server <br/>
2) Run the client
3) Input the required info prompted in the client's console
4) Check recipient's email

### The database will hold some key pieces of information:
1) Email ID (Primary key)
2) Sender's email address
3) Recipient's email address
4) Subject of email
5) Message body, encrypted with RSA encryption


### Purpose of project:
This application simply demonstrates how an email may be encrypted and decrypted as it is sent from one address to another using asymmetric encryption.
It may not be accurate to how emails are normally encrypted, but this was what I was able to envision for the final project of IFT 520 at Arizona State University.
The private key in the repository is meant to demonstrate what an RSA private key may look like. For the purposes of this application, it is mainly used to decrypt
data that is stored in the local database.
