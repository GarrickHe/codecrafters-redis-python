import socket

HOST = 'localhost'
PORT = 6379
BUF_SIZE_IN_BYTES = 1024


def simpleString(s):
    return str.encode('+' + s + '\r\n')


def main():
    print("{} listning on port: {}".format(HOST, PORT))
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    while True:
        conn, ipAddr = server_socket.accept()  # wait for client
        print('Connection from: {}'.format(ipAddr))
        conn.sendall(simpleString('PONG'))


if __name__ == "__main__":
    main()
