import time


from bokeh.models import ColumnDataSource, HoverTool

from bokeh.plotting import figure, curdoc
from functools import partial
from tornado.ioloop import IOLoop
import zmq.asyncio

doc = curdoc()

context = zmq.asyncio.Context.instance()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:1234")
socket.setsockopt(zmq.SUBSCRIBE, b"")


x = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y = [0,1,2,3,4,5,6,7,8,9,10,11,12]
yy = [0,2,4,3,4,8,6,7,2,9,1,2,12]
desc = [0,1,2,3,4,5,6,7,8,9,10,11,12]

previdx = 12
prev_data_dict = dict(h=x[:], z=y[:], d=desc[:])
data_k = [k for k in prev_data_dict.keys()]  # ['h', 'z', 'd']

# config source
source = ColumnDataSource(data=dict(h=x, z=y, d=desc))

def update(new_data):  # stream
    source.stream(new_data, rollover=10)
def update1(whole_data):  # refresh
    # ref: https://discourse.bokeh.org/t/is-there-a-way-to-refresh-an-entire-plot-with-new-data-all-at-once/1906/8
    # ref: https://stackoverflow.com/questions/34970704/what-is-a-fast-and-proper-way-to-refresh-update-plots-in-bokeh-0-11-server-app
    source.data = whole_data

async def loop():
    while True:
        global previdx, prev_data_dict, data_k
        new_data = await socket.recv_pyobj()
        # doc.add_next_tick_callback(partial(update, new_data))  # next tick call update(new_data)
        if new_data['h'] == previdx:  # if old k 
            optimized_data_dict = {k: prev_data_dict[k][:-1] for k in data_k}  # del last
            for k in data_k:
                optimized_data_dict[k].extend(new_data[k])   # add new
            prev_data_dict = optimized_data_dict   # update prev
            doc.add_next_tick_callback(partial(update1, optimized_data_dict))  # refresh the old
        else:  # if new k
            previdx = new_data['h']  # update idx
            doc.add_next_tick_callback(partial(update, new_data))  # stream only new 

def plotfunc():
    # figure model
    tooltips = [
        ("index", "$index"),
        ("pos", "($x, $y)"),
        ("desc", "@d"), # -> derived in source 
    ]
    plot = figure(height=300)

    line = plot.line(x='h', y='z', source=source)
    plot.add_tools(HoverTool(renderers=[line], tooltips=tooltips, mode='vline'))
    return plot


ppp_model = plotfunc()
doc.add_root(ppp_model)
IOLoop.current().spawn_callback(loop)




