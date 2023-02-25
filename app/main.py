import socket
import asyncio

HOST = 'localhost'
PORT = 6379
BUF_SIZE_IN_BYTES = 1024
RESP_DELIMITER = b'\r\n'

cache = {}


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

def getKey(s : bytes) -> str:
    return s.split(RESP_DELIMITER)[4].decode()

def getVal(s : bytes) -> str:
    return s.split(RESP_DELIMITER)[6].decode()

def setKeyVal(key : str, val : str) -> str:
    ret = cache[key] if key in cache else ""
    cache[key] = val
    return ret

def getKey(key : str) -> str:
    return cache[key] if key in cache else ""

async def handler(reader, writer):
    print(f'Connection from: {writer.get_extra_info("peername")}')
    while True:
        data = (await reader.read(BUF_SIZE_IN_BYTES))
        if len(data) == 0:
            break
        
        cmd = respCmd(data)

        if cmd == 'ECHO':
            writer.write(bulkString(respArg(data)))
        elif cmd == 'PING':
            if respLen(data) == 1:
                writer.write(simpleString('PONG'))
            else:
                writer.write(bulkString(respArg(data)))
        elif cmd == 'GET':
            writer.write(bulkString(getKey(getKey(data))))
        elif cmd == 'SET':
            ret = setKeyVal(getKey(data), getVal(data))
            if len(ret) == 0:
                writer.write(simpleString('OK'))
    writer.close()


async def main():
    print("{} listning on port: {}".format(HOST, PORT))
    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
