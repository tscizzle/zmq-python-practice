"""
USAGE:
Start the sink and workers before starting the ventilator which sends out work
`python parallel_pipeline.py` to start the ventilator
`python parallel_pipeline.py worker` to start a worker, of which there can be
multiple
`python parallel_pipeline.py sink` to start the sink
"""


import zmq
import time
import random
import sys


VENTILATOR_PORT = 5555
SINK_PORT = 5556

NUM_JOBS = 100

def ventilator():
    context = zmq.Context()
    work_socket = context.socket(zmq.PUSH)
    print("To send to workers, binding to port: %s" % VENTILATOR_PORT)
    work_socket.bind("tcp://*:%s" % VENTILATOR_PORT)

    sink_socket = context.socket(zmq.PUSH)
    print("To send to sink, connecting to port: %s" % SINK_PORT)
    sink_socket.connect("tcp://localhost:%s" % SINK_PORT)

    print("Once the workers are ready, press Enter to begin...")
    input()

    sink_socket.send_string("START MESSAGE, WHATEVER")

    total_work = 0

    for _ in range(NUM_JOBS):
        rand_work = random.randint(1, 100)

        total_work += rand_work

        data = str(rand_work)
        work_socket.send_string(data)
        print("Sent data: %s" % data)

    print("Expected work time: %s ms" % total_work)

def worker():
    context = zmq.Context()
    vent_socket = context.socket(zmq.PULL)
    print("To receive work, connecting to port: %s" % VENTILATOR_PORT)
    vent_socket.connect("tcp://localhost:%s" % VENTILATOR_PORT)

    sink_socket = context.socket(zmq.PUSH)
    print("To indicate work done, connecting to port: %s" % SINK_PORT)
    sink_socket.connect("tcp://localhost:%s" % SINK_PORT)

    MS = 0.001

    while True:
        data = vent_socket.recv_string()
        print("Received data: %s" % data)

        work_amount = int(data)
        time.sleep(work_amount * MS)

        sink_socket.send_string("Did a work")

def sink():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    print("Binding to port: %s" % SINK_PORT)
    socket.bind("tcp://*:%s" % SINK_PORT)

    socket.recv_string()

    start_time = time.time()

    for _ in range(NUM_JOBS):
        socket.recv_string()

    end_time = time.time()

    total_time = (end_time - start_time) * 1000

    print("Took %s ms" % total_time)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "worker":
            worker()
        elif sys.argv[1] == "sink":
            sink()
    else:
        ventilator()


if __name__ == "__main__":
    main()
