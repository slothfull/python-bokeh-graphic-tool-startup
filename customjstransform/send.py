import time
import random
import zmq
import numpy as np

context = zmq.Context.instance()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://127.0.0.1:1234")

t = 12 
tt = 12 
y = 0

while True:
    time.sleep(1.0)
    t += 1 
    tt += 1
    # y += random.normalvariate(0, 1)

    '''√ original'''
    pub_socket.send_pyobj(    dict(h=[t], z=[tt], d=[t])       )



