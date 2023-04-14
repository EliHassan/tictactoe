import socket
import time

port=5131
count = 0

with socket.socket() as s:
    s.connect(('localhost',port))
    while True:
        if count == 0:
            name = input('Enter Name to Start Your Game:')
            print("Ask other player to open terminal, launch game and Enter Name.")
            data = s.recv(1024)
            print(data.decode())
            count += 1
        else:
            field = input('Enter The Field Number:')
            print('Waiting for other palyers input..')
            s.send(field.encode())
            data = s.recv(1024)
            print("Its Your Turn")
            print(data.decode())
            data2 = s.recv(1024)
            if data2.decode() != '123':
                print(data2.decode())
                time.sleep(10)
                break