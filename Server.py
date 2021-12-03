import socket
import threading

host = '127.0.0.1'
port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            client.close()
            nickname = nicknames[index]
            broadcast('{} saiu da sala!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)

def receive():
    while True:
        client, address = server.accept()
        print("Conectado com {}".format(str(address)))

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        if(nicknameCheck(nickname)):
            client.send('Nickname já existente, escolha outro nome'.encode('utf-8'))
        nicknames.append(nickname)
        clients.append(client)

        print("Usuario: {}".format(nickname))
        broadcast("{} entrou na sala!".format(nickname).encode('utf-8'))
        client.send('Conectado ao servidor!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def nicknameCheck(nickname):
    exists = nickname in nicknames
    return exists

def userConnecteds(client):
    client.send('Usuarios conectados: {}'.format(nicknames).encode('utf-8'))

def nickanameChange(nickname,newNickname,client):
    nicknames.remove(nickname)
    nicknames.append(newNickname)
    broadcast('{} mudou o nickname para {}'.format(nickname,newNickname.encode('utf-8')))

receive()