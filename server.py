import socket
import threading

HOST_IP =  socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((HOST_IP , HOST_PORT))
server.listen()

clients = []
all_messages = []

def brodcast(message):
  for client in clients:
    client.send(message)

  
def valid(client):
  clients.append(client)
  for messages in all_messages:
      clients[-1].send(messages+'\n'.encode(ENCODER))
  
  while True: 
      try :
        message  = client.recv(BYTESIZE)
        if message == 'cls':
          all_messages.clear()
          all_messages.append(message)
          brodcast(message)
        all_messages.clear()
        all_messages.append(message)
        brodcast(message)
      except:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        break



def recieve():
  while True:
    client , add = server.accept()
    vt = threading.Thread(target=valid , args=(client,))
    vt.start()

    
  
recieve()