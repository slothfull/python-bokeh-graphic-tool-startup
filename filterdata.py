import os
import pandas as pd
import numpy as np

from bokeh.plotting import figure, show
from bokeh.transform import transform
from bokeh.models import CustomJSTransform, ColumnDataSource


def _read_file(filename):
    from os.path import dirname, join
    curpath = dirname(__file__)
    dfdata = pd.read_csv(join(curpath, filename), index_col=0, parse_dates=True, infer_datetime_format=True)
    return dfdata 

def SMA(arr: pd.Series, n: int) -> pd.Series:
    '''Returns n-period simple moving average of array arr.'''
    return pd.Series(arr).rolling(n).mean()

def convert(lst):
    tmp = np.array(lst)
    return np.where(np.isnan(tmp), None, tmp)


# daily NASDAQ:GOOG (Google/Alphabet) stock price data from 2004 to 2013
GOOG = _read_file('GOOG.csv') 
data = GOOG[0:4]
opening = data.Open  # series(2148,) index=datetime
closing = data.Close  # series(2148,) index=datetime
high = data.High  # series(2148,) index=datetime
low = data.Low  # series(2148,) index=datetime
volume = data.Volume  # series(2148,) index=datetime
mdot = (high+low+closing)/3  # set v5 for main-graph, series(2148,) index=datetime
sdot = (high+low+3*closing)/5  # set v5 for sub-graph, series(2148,) index=datetime
sma13 = SMA(mdot, 13)  # (13)
sma13lst = sma13.to_list()
converted_sma13lst = convert(sma13lst)
data_dict = {}
data_dict['idx'] = np.arange(sma13.size).tolist()
data_dict['val'] = converted_sma13lst.tolist()

# using js script to convert None(null) to Nan
f = """
    const a = NaN
    const ratio = 0.8 
    const norm = new Float64Array(xs.length);
    for (let i = 0; i < xs.length; i++) {
        if (xs[i] === null){
            norm[i] = a;
        }
        else{
            norm[i] = xs[i];
        }
    }
    return norm
    """
normalize = CustomJSTransform(v_func=f)
p = figure(title = "Iris Morphology")
p.line(x='idx', y=transform('val', normalize), line_width=8, color='#cf3c4d', alpha=0.6, legend_label="Apple", source=data_dict)
p.line(x='idx', y='val', line_width=2, color='#bffedd', alpha=0.6, legend_label="banana", source=data_dict)

p.xaxis.axis_label = 'Petal Length'
p.yaxis.axis_label = 'Sepal Width'

show(p)
