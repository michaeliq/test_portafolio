from flask import send_from_directory
from app import AppFlask
import os

'''
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("localhost",8086))
sock.setblocking(False)
sock.listen(10)

try:
    def acceptConn(sock=sock):
        while True:
            try:
                conn,addr=sock.accept()
                conn.setblocking(False)
                print(conn)
            except:
                pass
    while True:
        ask = input()
        if ask == "salir":
            sock.close()
            sys.exit()
            print('close socket connection')
            break


    accept_pro = threading.Thread(target=acceptConn)
    accept_pro.daemon = True
    accept_pro.start()
    
except:
    pass
'''

setting_module = os.getenv('APP_SETTINGS_MODULE')

app = AppFlask.create_app(setting_module)


