'''
客户端
'''
import socket

# 创建TCP套接字
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

file_name = input('请输入要下载的文件名：')
# 连接客户端
tcp_client_socket.connect(('127.1.1.2', 8080))
# 发送请求
tcp_client_socket.send(file_name.encode('utf-8'))
# 接收数据
with open('new' + file_name, 'wb') as file:
    while True:
        file_data = tcp_client_socket.recv(1024)
        if file_data:
            file.write(file_data)
        else:
            break
    print('下载完成')
# 关闭socket
tcp_client_socket.close()
