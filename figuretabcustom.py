from bokeh.plotting import save, figure, show
from bokeh.models import Paragraph, Panel, Tabs, Column

template = ''' 
           {% block postamble %}
           <style>
           .bk-root .bk-tabs-header .bk-tab {
               background-color: white;
               width: 50px;
               color: grey;
               font-style: normal;
               font-weight: bold;
               position: relative;
               left: 400px; 
           }
           .bk-root .bk-tabs-header .bk-tab.bk-active{
               background-color: #efefef;
               color: black;
               font-style: normal;
               font-weight: bold;
               position: relative;
               left: 400px;
           }
           .bk-root .bk-tabs-header .bk-tab:hover{
               background-color: yellow
               position: relative;
               left: 400px;
           }
           </style>
           {% endblock %}
           ''' 

p = Paragraph(text = "Another tab", width = 600)

plot = figure()
plot.line(x = [1, 2], y = [3, 4])
tabs = [Panel(title = 'Tab1', child = plot)]
tabs.append(Panel(title = 'Tab2', child = p))

show(Column(Tabs(tabs = tabs, width = 600, tabs_location='below')), template = template)



