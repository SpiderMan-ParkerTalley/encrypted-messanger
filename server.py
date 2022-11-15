from cryptography.fernet import Fernet
import socket

# Make sure to set these values appropriately before launching the program.
ip_addr = "localhost"
port = 12345

print("STARTING SERVER...")

# Generate a key to be used by the cipher.
key = Fernet.generate_key()
print("GENERATED KEY: ", str(key))

# Pass the key into the cipher and set the cipher to a variable that we can call.
cipher = Fernet(key)

# Create and store a socket that we can use to send and receive internet traffic.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, port))
server.listen()
print("ESTABLISHED SERVER\nIP ADDRESS: " + str(ip_addr) + "\nPORT: " + str(port))

# Wait for the client to establish a connect to the server.
print("WAITING FOR CLIENT TO CONNECT...")
client, addr = server.accept()
print("CLIENT CONNECTED")

# Send the key to the client so that it can encrypt and decrypt the following 
# messages.
client.send(key)
print("SENT KEY TO CLIENT")

# Continue to send and receive messages until changed to True.
done = False

print("WAITING FOR MESSAGE FROM CLIENT...")
while not done:
    
    # Receive, decode and decrypt the message received
    received = cipher.decrypt(client.recv(1024)).decode('utf-8')
    
    # Check if the message sent was to end the service and close.
    if received == 'quit':
        print("QUIT RESPONSE RECEIVED FROM CLIENT, CLOSING MESSENGER")
        done = True
    
    # If 'quit' was not sent, display the message to the user and ask the user
    # to send a response. Then encrypt the response and send it to the client.
    else:
        print(received)
        send = input("Message: ")
        
        # If the user wants to send 'quit' send the message to the client and 
        # close the server.
        if send == 'quit': 
            client.send(cipher.encrypt(bytes(send, 'utf-8')))
            done = True
        else:
            client.send(cipher.encrypt(bytes(send, 'utf-8')))

# Close the socket before the program closes.   
server.close()