from cryptography.fernet import Fernet
import socket

print("STARTING CLIENT...")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))
print("CONNECTED TO SERVER...")

print("WAITING FOR KEY...")
key = client.recv(1024)
print("KEY RECIEVED: " + str(key))

cipher = Fernet(key)

done = False

while not done:
    send = input("Message: ")
    if send == 'quit':
        client.send(cipher.encrypt(bytes(send, 'utf-8')))
        done = True
    else:
        client.send(cipher.encrypt(bytes(send, 'utf-8')))
        recieved = cipher.decrypt(client.recv(1024)).decode('utf-8')
        if recieved == 'quit':
            print("QUIT RESPONSE RECEIVED FROM SERVER, CLOSING MESSANGER")
            done = True
        else:
            print(recieved)