import socket
import threading

comando = input("Para entrar na sala digite /ENTRAR \n")

while(comando!= "/ENTRAR"):
    comando = input("Para entrar na sala digite /ENTRAR \n")

ip = input("Digite o IP do servidor: ")
port = int(input("Digite a porta do servidor: "))
nickname = input("Digite seu nome de usuario: ")
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((ip,port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ocorreu um erro!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname,input(''))
        client.send(message.encode('utf-8'))

receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()