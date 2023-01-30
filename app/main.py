import socket
import threading

HOST = 'localhost'
PORT = 6379
BUF_SIZE_IN_BYTES = 1024


def simpleString(s):
    return str.encode('+' + s + '\r\n')

def handler(conn):
    conn.sendall(simpleString('PONG'))
    conn.close()

def main():
    print("{} listning on port: {}".format(HOST, PORT))
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    conn, ipAddr = server_socket.accept()  # wait for client
    print('Connection from: {}'.format(ipAddr))
    while True:
        data = conn.recv(BUF_SIZE_IN_BYTES)
        if len(data) == 0:
            break
        conn.sendall(simpleString('PONG'))
    conn.close()

if __name__ == "__main__":
    main()
