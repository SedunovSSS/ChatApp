import socket
from tkinter import *
from tkinter import ttk
import threading
import sys
from playsound import playsound
import json
import pickle

s = socket.socket() 

host_data = json.load(open('host.json'))

host = host_data['HOST']
port = host_data["PORT"]

s.connect((host, port))

root = Tk()
root.title('Login Form')
root.iconbitmap('icons/icon.ico')

total_name = None
BUFF_SIZE = 1024*1024

def login():
    global total_name
    name = ent.get()
    s.send(name.encode('utf8'))
    if s.recv(BUFF_SIZE).decode('utf8') == 'success':
        total_name = name
        root.destroy()
        s.send(' '.encode('utf8'))
        return
    error_label.config(text='User already exists')

error_label = Label(text='', fg='red')
error_label.pack()

ent = Entry(width=40)
ent.pack(side='left', pady=5)

btn = Button(text='login', command=login, bg='black', fg='white')
btn.pack(side='right', pady=5)

root.mainloop()

root = Tk()
root.title(f'{total_name} - ChatApp')
root.iconbitmap('icons/icon.ico')

def send_message():
    message = ent.get()
    ent.delete(0, END)
    if message != '':
        s.send(message.encode('utf8'))

def recipe():
    while True:
        try:
            r = s.recv(BUFF_SIZE)
            print(pickle.loads(r))
            if r:
                r = pickle.loads(r)
                # print(r)
                listbox.insert(END, r['message'])
                listbox.yview(END)

                online_label.config(text=f"Online: {r['online']}")

                s_name = r['message'].split(': ')[0]
                if s_name != total_name and s_name != '[+] SYSTEM MESSAGE [+]':
                    playsound('sounds/sound.mp3')
        except:
            break

def on_closing():
    s.close()
    proc.join()
    root.destroy()
    sys.exit()


f = Frame()
f.pack(side="bottom", fill="y")

ent = Entry(f, width=40)
ent.pack(side="left")

btn = Button(f, text='send', command=send_message, bg='black', fg='white')
btn.pack(side="right")

online_label = Label(text='Online: ?', fg='blue')
online_label.pack(side='bottom')

scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side="right", fill="y")

listbox = Listbox(yscrollcommand=scrollbar.set, width=50)
listbox.pack(side="left", fill="both", expand=True)

proc = threading.Thread(target=recipe, args=())
proc.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
