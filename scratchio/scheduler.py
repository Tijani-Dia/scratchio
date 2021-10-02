import time
import types
import selectors
import socket

from base64 import b64encode
from hashlib import sha1
from collections import deque, namedtuple

from .priority_queue import PriorityQueue

SLEEPING = "__sleeping__"
ConnectionHandler = namedtuple("ConnectionHandler", ["reader", "writer"])

FIN = 0x80
RSV1 = 0x40
RSV2 = 0x20
RSV3 = 0x10
OPCODE = 0x0f
MASKED = 0x80
PAYLOAD_LEN = 0x7f



class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.scheduled = PriorityQueue()
        self.selector = selectors.DefaultSelector()
        self.current = None
        self.running = False
        self.serving = False
        self.handshake_done = False

    def close(self):
        self.running = False

    def call_soon(self, coro):
        self.ready.append(coro)

    def call_later(self, coro, delay):
        when = time.monotonic() + delay
        self.call_at(coro, when)

    def call_at(self, coro, when):
        self.scheduled.insert_item_with_priority(item=coro, priority=when)

    @types.coroutine
    def sleep(self, delay):
        when = time.monotonic() + delay
        self.call_at(self.current, when)
        yield SLEEPING

    def run(self):
        self.running = True
        while self.running:
            while self.ready:
                self.current = self.ready.popleft()
                try:
                    result = self.current.send(None)
                except StopIteration:
                    continue
                else:
                    if result == SLEEPING:
                        continue
                    self.call_later(self.current, 0)
            self.current = None


            if self.serving:
                event_list = self.selector.select()
                self.process_events(event_list)

            while not self.scheduled.is_empty():
                hp_item = self.scheduled.peek()
                now = time.monotonic()
                if hp_item.priority > now:
                    break

                hp_item = self.scheduled.pull_highest_pritority_item()
                self.ready.append(hp_item)

            if not self.ready and self.scheduled.is_empty():
                self.running = False
                return

    def start_serving(self, host, port):
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen()
        server_socket.setblocking(False)
        self.selector.register(server_socket, selectors.EVENT_READ, ConnectionHandler(reader=self.accept, writer=None))
        self.serving = True
        if not self.running:
            self.run()
        self.selector.unregister(server_socket)
        server_socket.close()
        self.serving = False

    def process_events(self, event_list):
        for key, mask in event_list:
            fileobj, (reader, writer) = key.fileobj, key.data

            if mask & selectors.EVENT_READ and reader is not None:
                self.call_soon(reader(fileobj, mask))

            if mask & selectors.EVENT_WRITE and writer is not None:
                self.call_soon(writer(fileobj, mask))

    async def accept(self, sock, mask):
        client_socket, address = sock.accept()  # Should be ready
        client_socket.setblocking(False)
        self.selector.register(client_socket, selectors.EVENT_READ, ConnectionHandler(reader=self.reader, writer=None))

    async def reader(self, client_socket, mask):
        data = client_socket.recv(1000)  # Should be ready
        if data:
            if not self.handshake_done:
                headers = self.parse_headers(data.decode())
                key = headers["Sec-WebSocket-Key"]
                response = self.make_handshake_response(key)
                print('Handshake')
                client_socket.send(response.encode())  # Hope it won't block
                self.handshake_done = True
            else:
                self.handle_message(data)
            
        else:
            print('closing', client_socket)
            self.selector.unregister(client_socket)
            client_socket.close()

    def handle_message(self, data):
        h1, h2 = data[:2]
        fin = h1 & FIN
        rsv1 = h1 & RSV1
        rsv2 = h1 & RSV2
        rsv3 = h1 & RSV3
        opcode = h1 & OPCODE
        masked = h2 & MASKED
        len_payload = h2 & PAYLOAD_LEN

        
        if not masked:
            return

        mask = bytes(data[2:6])
        encoded = bytes(data[-len_payload:])
        decoded = []
        for i in range(len_payload):
            decoded.append(encoded[i] ^ mask[i%4])
        breakpoint()
        got = decoded


        

    def parse_headers(self, data):
        headers = {}
        values = data.splitlines()
        for val in values:
            try:
                k, v = val.split(":", maxsplit=1)
            except ValueError:
                get_req = val
                continue
            headers[k] = v.strip()
        return headers

    @classmethod
    def make_handshake_response(cls, key):
        return \
          'HTTP/1.1 101 Switching Protocols\r\n'\
          'Upgrade: websocket\r\n'              \
          'Connection: Upgrade\r\n'             \
          'Sec-WebSocket-Accept: %s\r\n'        \
          '\r\n' % cls.calculate_response_key(key)

    @classmethod
    def calculate_response_key(cls, key):
        GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        hash = sha1(key.encode() + GUID.encode())
        response_key = b64encode(hash.digest()).strip()
        return response_key.decode('ASCII')