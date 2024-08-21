'''
服务端
'''
import socket

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
tcp_server_socket.bind(('127.1.1.2', 8080))
tcp_server_socket.listen(128)
while True:
    try:
        new_client_socket, client_addr = tcp_server_socket.accept()
        print('客户端{}上线了...'.format(client_addr))
        file_name = new_client_socket.recv(1024)
        print('收到请求：', file_name)
        with open('./files/' + file_name.decode('utf-8'), 'rb') as file:
            while True:
                file_data = file.read()
                if file_data:
                    new_client_socket.send(file_data)
                else:
                    print('文件发送完毕...')
                    break
    except Exception as e:
        print(e)
        break
    new_client_socket.close()
tcp_server_socket.close()