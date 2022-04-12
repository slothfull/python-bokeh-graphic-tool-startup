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
i = 0
while True:
    time.sleep(1.0)
    i+=1         # i:   1   2   3   4   5    6   7   8   9  10   11  12
    if(i%23==0):  #idx: 12  12  13  13  13   14  14  14  15  15  15  16
        t+=1
    else:
        t=t
    tt += 1
    # y += random.normalvariate(0, 1)

    '''√ original'''
    pub_socket.send_pyobj(    dict(h=[t], z=[tt], d=[t])       )



