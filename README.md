Walk Through

Start Server.py

Start up to 3 Client.py (any additional ones are told that the server is full 
Each client will then be prompted to name themselves by sending a message to the server which will then send a reply back indicating that they have been successfully named 

Now clients can send messages; if they are not recognized commands, they will receive an ACK from the server while all other clients will see that that client has sent a message

When a recognized command is sent, the server first ACKs the message before also sending the associated response from the server is sent back; in the case of using “get” with an invalid file name, the server will simply indicate that the file path is invalid.
