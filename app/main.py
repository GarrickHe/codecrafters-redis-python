import socket

HOST="localhost"
PORT=6379

def main():
    server_socket = socket.create_server((HOST, PORT), reuse_port=True)
    server_socket.accept() # wait for client
    print("{} listning on port: {}".format(HOST, PORT))

if __name__ == "__main__":
    main()
