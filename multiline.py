import os
import pandas as pd
import numpy as np

from bokeh.io import curdoc, show
from bokeh.plotting import figure, show
from bokeh.transform import transform, factor_cmap
from bokeh.models import CustomJSTransform, ColumnDataSource, Grid, LinearAxis, MultiLine, Plot
from bokeh.colors.named import (lime as BULL_COLOR, tomato as BEAR_COLOR)

def _read_file(filename):
    from os.path import dirname, join
    curpath = dirname(__file__)
    dfdata = pd.read_csv(join(curpath, filename), index_col=0, parse_dates=True, infer_datetime_format=True)
    return dfdata 

def EMA(arr: pd.Series, n:int) -> pd.Series:
    return pd.Series(arr).ewm(span=n, adjust=False, ignore_na=False).mean()

def GetLocalMaxMinIdx(arr: pd.Series):
    '''Returns local max min value->index'''
    num = arr.size
    vertex_idx = [] 
    _ = 0
    for _ in range(arr.size):
        if(_==0 or _==num-1):
            continue
        if(arr.iat[_]>arr.iat[_-1] and arr.iat[_]>arr.iat[_+1]):
            vertex_idx.append(_)
            continue
        if(arr.iat[_]<arr.iat[_-1] and arr.iat[_]<arr.iat[_+1]):
            vertex_idx.append(_)
            continue
    return vertex_idx 

def MidBolling(arr: pd.Series, vertexlst: list):
    '''Return the midbolling multiline and index'''
    subidxlst = []
    bollidxlst = []
    subdatalst = []
    bolldatalst = []
    for _ in range(arr.size):
        subidxlst.append(_)  # idx
        subdatalst.append(arr.iat[_])  # data
        if(_ in vertexlst):
            # idx
            bollidxlst.append(subidxlst)
            subidxlst = []
            subidxlst.append(_)
            # data
            bolldatalst.append(subdatalst)
            subdatalst = []
            subdatalst.append(arr.iat[_])
    bollidxlst.append(subidxlst)
    bolldatalst.append(subdatalst)
    return bolldatalst, bollidxlst 


# daily NASDAQ:GOOG (Google/Alphabet) stock price data from 2004 to 2013
GOOG = _read_file('GOOG.csv') 
data = GOOG[1:22]
opening = data.Open  # series(2148,) index=datetime
closing = data.Close  # series(2148,) index=datetime
high = data.High  # series(2148,) index=datetime
low = data.Low  # series(2148,) index=datetime
volume = data.Volume  # series(2148,) index=datetime
mdot = (high+low+closing)/3  # set v5 for main-graph, series(2148,) index=datetime

ema3 = EMA(mdot, 3)  # (0)
ema33 = EMA(ema3, 3)  # (0)
ema337 = EMA(ema33, 7)  # (0)

# [5, 14]
vertex = GetLocalMaxMinIdx(ema337)
# [1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1]
midbolling, idx = MidBolling(ema337, vertex)

xx = idx
yy = midbolling

source = ColumnDataSource(dict(
        xs=xx,
        ys=yy,
        colorsss=[['-1'], ['1'], ['-1']]
))
from bokeh.palettes import BuGn8
COLORS = [BuGn8[0], BuGn8[4]]
source_cmap = factor_cmap('colorsss', COLORS, ['-1', '1'])

p = figure(title = "Iris Morphology")
# p.multi_line(xs="xs", ys="ys", source=source, line_color='red', line_width=8)
p.multi_line(xs="xs", ys="ys", source=source, line_color=source_cmap, line_width=8)
show(p)

