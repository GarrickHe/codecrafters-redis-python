import socket
import asyncio

HOST = 'localhost'
PORT = 6379
BUF_SIZE_IN_BYTES = 1024


def simpleString(s):
    return str.encode('+' + s + '\r\n')


async def handler(reader, writer):
    print(f'Connection from: {writer.get_extra_info("peername")}')
    while True:
        data = (await reader.read(BUF_SIZE_IN_BYTES))
        if len(data) == 0:
            break
        writer.write(simpleString('PONG'))
    writer.close()


async def main():
    print("{} listning on port: {}".format(HOST, PORT))
    server = await asyncio.start_server(handler, HOST, PORT)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
