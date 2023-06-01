# coding: utf-8

import socket

ip1 = '127.0.0.1'
port1 = 8765
server1 = (ip1, port1)

socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

line = ''
while line != 'q':
    # 標準入力からデータを取得
    print('type z/x/q to StartRecord/StopRecord/Quit')
    line = input('>>>')
    
    # サーバに送信
    socket1.sendto(line.encode("UTF-8"),(ip1, port1))
    
socket1.close()
print('クライアント側終了です')