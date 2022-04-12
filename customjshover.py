import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Span
from bokeh.layouts import layout

plot1 = figure(plot_width=1000, plot_height=250)

df = pd.DataFrame({"ID":[0, 1, 2, 3, 4, 5, 6, 7], 
                   "Value1":[0, 100, 200, 300, 400, 500, 600, 700], 
                   "Value2":[0, 1, 2, 4, 8, 16, 32, 64]})
source = ColumnDataSource(df)

line = plot1.line(x='ID', y='Value1', source=source)
circle = plot1.circle(x='ID', y='Value1', source=source)
v_line = Span(location=2,  dimension='height', line_color='green', line_dash='dashed', line_width=3)
plot1.add_layout(v_line)

callback = CustomJS(
        args=dict(source=source, v_line=v_line), 
        code="""v_line.location = cb_data['index'].line_indices[0];source.change.emit();""")
hover_tool_plot = HoverTool(mode='vline', line_policy='nearest', callback=callback, renderers=[line])

plot1.add_tools(hover_tool_plot)

layout_ = layout([[plot1]])
curdoc().add_root(layout_)
