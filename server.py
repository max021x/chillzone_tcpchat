import socket
import threading
import sqlite3
HOST_IP =  socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = "utf-8"
BYTESIZE = 1024

connect_db = sqlite3.connect(r'db\info.db')
cur = sqlite3.Cursor(connect_db)

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((HOST_IP , HOST_PORT))
server.listen()

clients = []
nicknames = []
db = []

for row in cur.execute('SELECT Username , Password from chillzone'):
  db.append(row)

def brodcast(message):
  for client in clients:
    client.send(message)


  
def valid(client):
  flag = False
  while True:
    try:
      message = client.recv(BYTESIZE).decode(ENCODER).strip()
      newmessage = message.split(":")
      info = (newmessage[0] , newmessage[1])
      if (info in db)and newmessage[0] not in nicknames:
        client.send('enter'.encode(ENCODER))
        nicknames.append(newmessage[0])
        clients.append(client)
        flag = True
        break
      else:
        print("EROR")
        print(message)
        client.send('info'.encode(ENCODER))
    except:
      client.close()
      break
   
  while flag: 
      try :
        message  = client.recv(BYTESIZE)
        brodcast(message)
      except:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)
        break



def recieve():
  while True:
    client , add = server.accept()
    client.send('info'.encode(ENCODER))
    vt = threading.Thread(target=valid , args=(client,))
    vt.start()

    
  
recieve()