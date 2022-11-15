from cryptography.fernet import Fernet
import socket

ip_addr = "localhost"
port = 12345

print("STARTING SERVER...")

key = Fernet.generate_key()
print("GENERATED KEY: ", str(key))

cipher = Fernet(key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, port))
server.listen()
print("ESATABLISHED SERVER\nIP ADDRESS: " + str(ip_addr) + "\nPORT: " + str(port))

print("WAITING FOR CLIENT TO CONNECT...")
client, addr = server.accept()
print("CLIENT CONNECTED")

client.send(key)
print("SENT KEY TO CLIENT")

done = False

print("WAITING FOR MESSAGE FROM CLIENT...")
while not done:
    recieved = cipher.decrypt(client.recv(1024)).decode('utf-8')
    if recieved == 'quit':
        print("QUIT RESPONSE RECEIVED FROM CLIENT, CLOSING MESSANGER")
        done = True
    else:
        print(recieved)
        send = input("Message: ")
        if send == 'quit': 
            client.send(cipher.encrypt(bytes(send, 'utf-8')))
            done = True
        else:
            client.send(cipher.encrypt(bytes(send, 'utf-8')))