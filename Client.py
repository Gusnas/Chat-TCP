import socket
import threading

ipServer = "127.0.0.1"
portServer = 9999

comando = input("Para entrar na sala digite /ENTRAR \n")

while(comando!= "/ENTRAR"):
    comando = input("Para entrar na sala digite /ENTRAR \n")

ip = input("Digite o IP do servidor: ")
while(ip != ipServer):
    print("IP incorreto, tente novamente")
    ip = input("Digite o IP do servidor: ")

port = int(input("Digite a porta do servidor: "))
while(port != portServer):
    print("Porta incorreta, tente novamente")
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
            elif message == 'TROCARNICK':
                print("Digite seu nickname novo: ")
                newNickname = input()
                client.send(newNickname.encode('utf-8'))
            elif message == 'SAIR':
                print("Desconectado com sucesso!")
                client.close()
                break
            elif message == 'USUARIOS':
                print(message)
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