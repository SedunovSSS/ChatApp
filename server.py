import socket
from threading import Thread
import json
import pickle

def write_log(log):
    log_file = open('chatlogs.log', 'a', encoding='utf8')
    log_file.write(log)
    log_file.close()

def send2all_clients(why_send):
    for client in clients:
        client.sendall(why_send)

s = socket.socket() 

host_data = json.load(open('host.json'))

host = host_data['HOST']
port = host_data["PORT"]

s.bind((host, port))
s.listen(5)

clients = []
usernames = ['[+] SYSTEM MESSAGE [+]']

BUFF_SIZE = 1024*1024

write_log('[+] SYSTEM MESSAGE [+]: Application started\n')

def start_new_client(conn, addr):
    name = conn.recv(BUFF_SIZE).decode('utf8')
    while name in usernames:
        conn.send('exists'.encode('utf8'))
        name = conn.recv(BUFF_SIZE).decode('utf8')
    conn.send('success'.encode('utf8'))
    usernames.append(name)
    conn.recv(BUFF_SIZE)
    print(f'[+] SYSTEM MESSAGE [+]: {name} was been connected! {addr}')
    write_log(f'[+] SYSTEM MESSAGE [+]: {name} was been connected! {addr}\n')
    send2all_clients(pickle.dumps({'message': f'[+] SYSTEM MESSAGE [+]: {name} was been connected!', 'online': f'{len(clients)}'}))
    while True:
        try:
            message = conn.recv(BUFF_SIZE).decode('utf8')
            if message == '': 
                break
            print(f'[+] MESSAGE [+]: {name}: {message}')
            write_log(f'[+] MESSAGE [+]: {name}: {message}\n')
            send2all_clients(pickle.dumps({'message': f'{name}: {message}', 'online': f'{len(clients)}'}))
        except:
            break
    clients.remove(conn)
    usernames.remove(name)
    conn.close()
    print(f'[+] SYSTEM MESSAGE [+]: {name} leave!')
    write_log(f'[+] SYSTEM MESSAGE [+]: {name} leave!\n')
    send2all_clients(pickle.dumps({'message': f'[+] SYSTEM MESSAGE [+]: {name} leave!', 'online': f'{len(clients)}'}))

while True:
    conn, addr = s.accept()
    clients.append(conn)
    Thread(target=lambda: start_new_client(conn, addr)).start()

s.close()
