import socket
import threading

host = '127.0.0.1'
port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(4)

print("SERVER UP #DEBUG")

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client,nickname):
    while True:
        try:
            message = client.recv(1024)
            isCommand = commandCheck(message,nickname,client)
            if isCommand == False:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} saiu da sala!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        if(len(clients)<4):
            client, address = server.accept()
            print("Conectado com endereço {}".format(str(address)))
        else:
            client.message('Servidor lotado!'.encode('utf-8'))
            print("SERVIDOR LOTADO!!!")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        while(nicknameCheck(nickname)):
            client.send('Nickname já existente, escolha outro nome'.encode('utf-8'))
            nicknameTry = client.recv(1024).decode('utf-8')
            remove = nickname + ': '
            nickname = nicknameTry.replace(remove,'')

        nicknames.append(nickname)
        clients.append(client)

        print("Nickname: {}".format(nickname))
        broadcast("{} entrou na sala!".format(nickname).encode('utf-8'))
        client.send('Conectado ao servidor!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,nickname,))
        thread.start()

def nicknameCheck(nickname):
    exists = nickname in nicknames
    return exists

def userConnecteds(client, nickname):
    if len(clients) == 1:
        client.send('Apenas você {} está conectado nesta sala!'.format(nickname).encode('utf-8'))
    else:
        client.send('Usuarios conectados: {}'.format(nicknames).encode('utf-8'))

def nicknameChange(client, nickname):
    client.send('TROCARNICK'.encode('utf-8'))

    newNickname = client.recv(1024).decode('utf-8')
    remove = nickname + ': '
    newNickname = newNickname.replace(remove,'')

    for i in range(len(nicknames)):
        if nicknames[i] == nickname:
            nicknames[i] = newNickname

    broadcast('{} mudou o nickname para {}'.format(nickname,newNickname).encode('utf-8'))


def quitChat(client, nickname):
    if client in clients:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} saiu da sala!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)

def commandCheck(message,nickname,client):
    decodeMessage = message.decode('utf-8')
    if decodeMessage == nickname + ': /SAIR':
        quitChat(client, nickname)
        return True
    elif decodeMessage == nickname + ': /USUARIOS':
        userConnecteds(client, nickname)
        return True
    elif decodeMessage == nickname + ': /NICK':
        nicknameChange(client, nickname)
        return True
    else:
        return False

receive()