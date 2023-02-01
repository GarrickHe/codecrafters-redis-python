import socket
import asyncio

HOST = 'localhost'
PORT = 6379
BUF_SIZE_IN_BYTES = 1024
RESP_DELIMITER = b'\r\n'


def simpleString(s : str) -> bytes:
    return ('+' + s + '\r\n').encode()

def bulkString(s : str) -> bytes:
    return ('$' + str(len(s)) + '\r\n' + s + '\r\n').encode()

def respLen(s : bytes) -> int:
    return int(s.split(RESP_DELIMITER)[0].decode()[1:])

def respCmd(s : bytes) -> str:
    return s.split(RESP_DELIMITER)[2].decode()

def respArg(s : bytes) -> str:
    return s.split(RESP_DELIMITER)[4].decode()

async def handler(reader, writer):
    print(f'Connection from: {writer.get_extra_info("peername")}')
    while True:
        data = (await reader.read(BUF_SIZE_IN_BYTES))
        if len(data) == 0:
            break
        
        cmd = respCmd(data)

        if cmd == 'ECHO':
            writer.write(bulkString(respArg(data)))
        else:
            if respLen(data) == 1:
                writer.write(simpleString('PONG'))
            else:
                writer.write(bulkString(respArg(data)))
    writer.close()


async def main():
    print("{} listning on port: {}".format(HOST, PORT))
    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
