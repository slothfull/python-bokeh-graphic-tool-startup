import time
import random
import zmq
import numpy as np

context = zmq.Context.instance()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://127.0.0.1:1234")

t = 12 
tt = 12 
y = 10 

while True:
    time.sleep(1.0)
    t += 1 
    tt += 1
    y += random.normalvariate(0, 1)

    '''√ original'''
    pub_socket.send_pyobj((     dict(x=[t], y=[y]),   dict(h=[t], z=[tt], d=[str(t)])       ))

    '''× transfer dict with one key less: ValueError: Must stream updates to all existing columns (missing: d)'''
    # pub_socket.send_pyobj((     dict(x=[t], y=[y]),   dict(h=[tt], z=[2*y])       ))

    '''√ transfer empty dict'''
    # pub_socket.send_pyobj((     dict(x=[t], y=[y]),   {}       ))

    '''× transfer only 1 dict: ValueError: not enough values to unpack (expected 2, got 1)'''
    # pub_socket.send_pyobj((     dict(x=[t], y=[y]),            ))

    '''√ transfer None values'''
    # pub_socket.send_pyobj((     dict(x=[t], y=[y]),   dict(h=[t], z=[None], d=[str(t)])       ))

    '''× tarnsfer Nan values: ValueError: Out of range float values are not JSON compliant'''
    '''https://stackoverflow.com/questions/14162723/replacing-pandas-or-numpy-nan-with-a-none-to-use-with-mysqldb'''
    '''pandas convert none to nan when other values are all numeric types, need <where> to replace it for database etc.'''
    '''use Nan in numeric value configuration stage, use None in database scenarios.'''
    # pub_socket.send_pyobj((     dict(x=[t], y=[y]),   dict(h=[np.nan], z=[2*y], d=[str(tt)])       ))




