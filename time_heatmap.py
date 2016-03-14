import bacteriopop_utils
import feature_selection_utils
import load_data
import numpy as np
import pandas as pd
import math

from math import pi
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure, show, output_file

def select_sample(oxygen,replicate):
    dataframe = load_data.load_data()
    
    if (oxygen == "Low") or (oxygen == 'low'):
        dataframe = dataframe[dataframe['oxygen'] == 'Low']
    if (oxygen == "High") or (oxygen == "high"):
        dataframe = dataframe[dataframe['oxygen'] == 'High']
        
    if (replicate == 1):
        dataframe = dataframe[dataframe['replicate'] == 1]
    if (replicate == 2):
        dataframe = dataframe[dataframe['replicate'] == 2]
    if (replicate == 3):
        dataframe = dataframe[dataframe['replicate'] == 3]
    if (replicate == 4):
        dataframe = dataframe[dataframe['replicate'] == 4]
        
    return dataframe

def set_data(df):
    df.replace('', 'other', inplace=True)
    df = df.drop(['kingdom','phylum','class','order','family','oxygen','replicate','length'],axis=1)
    df = df[(df['abundance'] >= 0.005)]
    df = df[(df.genus != 'other')]
    df['week'] = [str(x) for x in df['week']]
    df = df.set_index('week')
    return df

def set_plot(df):
    bact = list(pd.unique(df['genus'].ravel()))
    weeks = list(pd.unique(df.index.ravel()))
    name = []
    week = []
    color = []
    rate = []
    for y in weeks:
        for m in bact:
            name.append(m)
            week.append(y)
            df2 = df[(df.index == y)]
            abundance = df2[(df2.genus == m)].abundance.sum()
            rate.append(abundance)
            if abundance >=  0.3:
                colorx = "#550b1d"
            elif abundance >=  0.2:
                colorx = "#933b41"
            elif abundance >=  0.1:
                colorx = "#cc7878"
            elif abundance >=  0.05:
                colorx = "#ddb7b1"
            elif abundance >=  0.01:
                colorx = "#dfccce"
            elif abundance >=  0.006:
                colorx = "#e2e2e2"
            elif abundance >=  0.003:
                colorx = "#c9d9d3"
            elif abundance >=  0.001:
                colorx = "#a5bab7"
            else: 
                colorx = "#75968f"
            color.append(colorx)
    source = ColumnDataSource(
    data=dict(name=name, week=week, color=color, rate=rate))
    TOOLS = "resize,hover,save,pan,box_zoom,wheel_zoom"

    p = figure(title="Heat plot ",
           x_range=weeks, y_range=list(reversed(bact)),
           x_axis_location="above", plot_width=800, plot_height=800,
           toolbar_location="left", tools=TOOLS)
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.rect("week", "name", 1, 1, source=source,
       color="color", line_color=None)
    p.select_one(HoverTool).tooltips = [
    ('date', '@name @week'),
    ('rate', '@rate'),]
    
    return p

def draw(oxygen,replicate):
    df = select_sample(oxygen,replicate)
    df = set_data(df)
    p= set_plot(df)
    output_file('time_Heatmap.html', title="time_heatmap.py example")

    show(p)      # show the plot
    
    return