"""
USAGE:
`python pub_sub.py` to start the publisher
`python pub_sub.py subscriber` to start a subscriber, of which there can be
multiple
"""


import zmq
import time
import random
import sys


PORT = 5555

def publisher():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    print("Binding to port: %s" % PORT)
    socket.bind("tcp://*:%s" % PORT)

    running_sum = 0

    while True:
        rand_data = random.random() - 0.5
        running_sum += rand_data

        time.sleep(0.01)

        data = str(running_sum)
        socket.send_string(data)
        print("Sent data: %s" % data)

def subscriber():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    print("Connecting to port: %s" % PORT)
    socket.connect("tcp://localhost:%s" % PORT)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        data = socket.recv_string()
        print("Received data: %s" % data)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "subscriber":
        subscriber()
    else:
        publisher()


if __name__ == "__main__":
    main()
