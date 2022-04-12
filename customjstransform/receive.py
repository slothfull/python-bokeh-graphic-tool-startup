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


x2 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y2 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
desc = [0,1,2,3,4,5,6,7,8,9,10,11,12]
# desc = ['A', 'b', 'C', 'd', 'E', 'A', 'b', 'C', 'd', 'E', 'A', 'b', 'C']

# config source
source2 = ColumnDataSource(data=dict(h=x2, z=y2, d=desc))

# update source by stream method
def update2(new_data2):
    source2.stream(new_data2, rollover=10)

async def loop():
    while True:
        new_data, new_data2 = await socket.recv_pyobj()
        # print(new_data2)  # {'h': [15], 'z': [3.2179100917432124], 's': ['9']}
        doc.add_next_tick_callback(partial(update2, new_data2))  # next tick call update2(new_data2)


def plotfunc():
    # figure model
    tooltips2 = [
        ("index", "$index"),
        ("pos", "($x, $y)"),
        ("desc", "@d"), # -> derived in source 
    ]
    plot = figure(height=300)

    # delete every 4 dot in plot.line2 using customjstransform
    valid = """
            const a = NaN;
            const ratio = 0.8;
            const norm = new Float64Array(xs.length);
            for (let i = 0; i < xs.length; i++) {
                if(source.data['d'][i]%4==0){
                    norm[i] = a
                }
                else{
                    norm[i] = xs[i]
                }
            }
            return norm
            """
    from bokeh.models import CustomJSTransform
    from bokeh.transform import transform

    arg_dict = dict(source=source2)
    validation = CustomJSTransform(v_func=valid, args=arg_dict)  # for list obj not for list(list) like multi_line

    line2 = plot.line(x=transform('h', validation), y='z', legend_label='s', source=source2)
    plot.add_tools(HoverTool(renderers=[line2], tooltips=tooltips2, mode='vline'))
    return plot


ppp_model = plotfunc()
doc.add_root(ppp_model)
IOLoop.current().spawn_callback(loop)




