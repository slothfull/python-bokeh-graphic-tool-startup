import random
import pandas as pd
from tornado.ioloop import IOLoop
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CheckboxGroup, Panel, Tabs, WidgetBox, Row
from bokeh.palettes import Category10

# define 4 lines which can be classified into 4 groups
data = [['a', 1, 0], ['a', 2, 1], ['a1', 1, 0], ['a1', 2, 2], ['b', 1, 0], ['b', 2, 3], ['b1', 1, 0], ['b1', 2, 4]]
df = pd.DataFrame(data, columns = ['group', 'time', 'rate'])

def modify_doc(doc):
    lines = []

    def create_plots(to_plot):  # create figure model                                 
        for i in range(len(to_plot)):
            source = ColumnDataSource(
                data = {'x':df.loc[df.group == to_plot[i]].time,
                       'group':df.loc[df.group == to_plot[i]].group,
                       'y':df.loc[df.group == to_plot[i]].rate}
            )
            lines.append(p3.line(x = 'x',
                                 y = 'y',
                                 source = source,
                                 legend = to_plot[i],
                                 color = (Category10[10])[i]))
            p3.legend.click_policy = 'hide'

    def update(attr, old, new):  # group select & set attributes
        for i in [0, 1]:
            if i not in selection1.active:
                lines[i].visible = False
            else:
                lines[i].visible = True

        if selection2.active:
            if len(lines) < 3:
                temp = []
                for i in selection1.active:
                    lines[i].visible = True
                    for b in selection2.active:
                        temp.append(selection1.labels[i] + selection2.labels[b])
                create_plots(temp)
            else:
                for i in range(2, 4):
                    if (i - 2) in selection1.active:
                        lines[i].visible = True
                    else:
                        lines[i].visible = False
        elif len(lines) > 2:
            for i in range(2, 4):
                if (i - 2) in selection1.active:
                    lines[i].visible = False

    selection1 = CheckboxGroup(labels = ['a', 'b'], active = [0, 1], width = 40)
    selection1.on_change('active', update)
    selection2 = CheckboxGroup(labels = ['1'], width = 40)
    selection2.on_change('active', update)

    p3 = figure()
    create_plots(['a', 'b'])

    controls = WidgetBox(selection1, selection2, width = 40)
    layout = Row(controls, p3)
    tab = Panel(child = layout, title = 'test')
    tabs = Tabs(tabs = [tab])
    doc.add_root(tabs)

io_loop = IOLoop.current()
server = Server(applications = {'/myapp': Application(FunctionHandler(modify_doc))}, io_loop = io_loop, port = 5001)
server.start()
server.show('/myapp')
io_loop.start()

# show(app)
