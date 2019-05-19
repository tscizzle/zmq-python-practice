"""
USAGE:
`python rep_req.py` to start the server
`python rep_req.py client` to start a client, of which there can be multiple
"""


import zmq
import random
import time
import sys


PORT = 5555

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    print("Binding to port: %s" % PORT)
    socket.bind("tcp://*:%s" % PORT)

    while True:
        req = socket.recv_string()
        print("Received request: %s" % req)

        time.sleep(1)

        resp = "Nice to meet you, %s" % req
        socket.send_string(resp)
        print("Sent response: %s" % resp)

def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    print("Connecting to port: %s" % PORT)
    socket.connect("tcp://localhost:%s" % PORT)

    first_names = ['Janice', 'Kim', 'Anurag', 'Carlos', 'Berrick']
    last_names = ['Rose', 'Kim', 'Platanos', 'Spade', 'Crater']
    client_name = random.choice(first_names) + ' ' + random.choice(last_names)

    while True:
        req = client_name
        socket.send_string(req)
        print("Sent request: %s" % req)

        resp = socket.recv_string()
        print("Received response: %s" % resp)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        client()
    else:
        server()


if __name__ == "__main__":
    main()
