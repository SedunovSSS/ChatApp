import socket
from threading import Thread

def write_log(log):
    log_file = open('chatlogs.log', 'a', encoding='utf8')
    log_file.write(log)
    log_file.close()

s = socket.socket() 
host = '127.0.0.1'
port = 1488

s.bind((host, port))
s.listen(5)

clients = []
usernames = []

write_log('[+] SYSTEM MESSAGE [+]: Application started\n')

def start_new_client(conn, addr):
    name = conn.recv(1024).decode('utf8')
    while name in usernames:
        conn.send('exists'.encode('utf8'))
        name = conn.recv(1024).decode('utf8')
    conn.send('success'.encode('utf8'))
    usernames.append(name)
    conn.recv(1024)
    print(f'[+] SYSTEM MESSAGE [+]: {name} was been connected! {addr}')
    write_log(f'[+] SYSTEM MESSAGE [+]: {name} was been connected! {addr}\n')
    for client in clients:
        client.sendall(f'[+] SYSTEM MESSAGE [+]: {name} was been connected!'.encode('utf8'))
    while True:
        try:
            message = conn.recv(1024).decode('utf8')
            if message == '': 
                break
            print(f'[+] MESSAGE [+]: {name}: {message}')
            write_log(f'[+] MESSAGE [+]: {name}: {message}\n')
            for client in clients:
                client.sendall(f'{name}: {message}'.encode('utf8'))
        except:
            break
    clients.remove(conn)
    usernames.remove(name)
    conn.close()
    print(f'[+] SYSTEM MESSAGE [+]: {name} leave!')
    write_log(f'[+] SYSTEM MESSAGE [+]: {name} leave!\n')
    for client in clients:
        client.sendall(f'[+] SYSTEM MESSAGE [+]: {name} leave!'.encode('utf8'))


while True:
    conn, addr = s.accept()
    clients.append(conn)
    Thread(target=lambda: start_new_client(conn, addr)).start()

s.close()