from bokeh.plotting import figure, show
from bokeh.models import Slider, CustomJSFilter, CDSView, ColumnDataSource, CustomJS
from bokeh.layouts import column, layout

# data/source
data = dict(Flights=[97, 34, 23, 6, 26, 97, 21, 92, 73, 10, 92, 14, 77, 4, 25, 48, 26, 39, 93],
            Not_Cancelled=[87, 63, 56, 38, 57, 63, 73, 56, 30, 23, 66, 47, 76, 15, 80, 78, 69, 87, 28],
            OnTime_Arrivals=[21, 65, 86, 39, 32, 62, 46, 51, 17, 79, 64, 43, 54, 50, 47, 63, 54, 84, 79])
source = ColumnDataSource(data=data)

# force a re-render when the slider changes
minflights = Slider(start=0, value=50, end=100, step=1)
minflights.js_on_change('value', CustomJS(args=dict(source=source), code="""source.change.emit()"""))

# cdsview filter
custom_filter = CustomJSFilter(args=dict(slider=minflights), code="""
    const indices = []
    for(var i=0; i<source.get_length(); i++){
        if(source.data['Flights'][i]>slider.value){
            indices.push(true)
        }
        else{
            indices.push(false)
        }
    }
    return indices
""")

p = figure()
view = CDSView(source=source, filters=[custom_filter])  # control the visulize of the source data
p.circle('OnTime_Arrivals', 'Not_Cancelled', source=source, view=view, size=20)  # view controled plot segment
inputs = column(minflights, width=200)  # slider widget

show(layout([[inputs,p]]))


