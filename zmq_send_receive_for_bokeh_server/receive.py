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


x1 = [0,1,2,3,4,5,6,7]
y1 = [0,1,2,3,4,3,2,1]
x2 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y2 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
# desc = [0,1,2,3,4,5,6,7,8,9,10,11,12]
desc = ['A', 'b', 'C', 'd', 'E', 'A', 'b', 'C', 'd', 'E', 'A', 'b', 'C']

# config source
source = ColumnDataSource(data=dict(x=x1, y=y1))
source2 = ColumnDataSource(data=dict(h=x2, z=y2, d=desc))

# update source by stream method
def update(new_data):
    source.stream(new_data, rollover=10)
def update2(new_data2):
    source2.stream(new_data2, rollover=10)

async def loop():
    while True:
        new_data, new_data2 = await socket.recv_pyobj()
        # print(new_data2)  # {'h': [15], 'z': [3.2179100917432124], 's': ['9']}
        doc.add_next_tick_callback(partial(update, new_data))  # next tick call update(new_data)
        doc.add_next_tick_callback(partial(update2, new_data2))  # next tick call update2(new_data2)


def plotfunc():
    # figure model
    tooltips1 = [
        ("index", "$index"),
        ("pos", "($x, $y)"),
    ]
    tooltips2 = [
        ("index", "$index"),
        ("pos", "($x, $y)"),
        ("desc", "@d"), # -> derived in source 
    ]

    plot = figure(height=300)
    # 1
    line1 = plot.line(x='x', y='y', source=source)
    plot.add_tools(HoverTool(renderers=[line1], tooltips=tooltips1, mode='vline'))
    # 2
    line2 = plot.line(x='h', y='z', legend_label='s', source=source2)
    plot.add_tools(HoverTool(renderers=[line2], tooltips=tooltips2, mode='vline'))
    return plot


ppp_model = plotfunc()
doc.add_root(ppp_model)
IOLoop.current().spawn_callback(loop)




