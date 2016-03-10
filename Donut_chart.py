import bacteriopop_utils
import feature_selection_utils
import load_data
import numpy as np
import pandas as pd

from bokeh.charts import Donut, show, output_file
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data

def select_sample(oxygen,week,replicate):
    dataframe = load_data.load_data()
    
    if (oxygen == "Low") or (oxygen == 'low'):
        dataframe = dataframe[dataframe['oxygen'] == 'Low']
    if (oxygen == "High") or (oxygen == "high"):
        dataframe = dataframe[dataframe['oxygen'] == 'High']
        
    if (week == 4):
        dataframe = dataframe[dataframe['week'] == 4]
    if (week == 5):
        dataframe = dataframe[dataframe['week'] == 5]
    if (week == 6):
        dataframe = dataframe[dataframe['week'] == 6]
    if (week == 7):
        dataframe = dataframe[dataframe['week'] == 7]
    if (week == 8):
        dataframe = dataframe[dataframe['week'] == 8]
    if (week == 9):
        dataframe = dataframe[dataframe['week'] == 9]
    if (week == 10):
        dataframe = dataframe[dataframe['week'] == 10]
    if (week == 11):
        dataframe = dataframe[dataframe['week'] == 11]
    if (week == 12):
        dataframe = dataframe[dataframe['week'] == 12]
    if (week == 13):
        dataframe = dataframe[dataframe['week'] == 13]
    if (week == 14):
        dataframe = dataframe[dataframe['week'] == 14]
        
    if (replicate == 1):
        dataframe = dataframe[dataframe['replicate'] == 1]
    if (replicate == 2):
        dataframe = dataframe[dataframe['replicate'] == 2]
    if (replicate == 3):
        dataframe = dataframe[dataframe['replicate'] == 3]
    if (replicate == 4):
        dataframe = dataframe[dataframe['replicate'] == 4]
        
    return dataframe

def reduce_data(df):
    df = bacteriopop_utils.reduce_data(df, 0.02, phylo_column='genus', oxygen="all")
    df = df.drop(['oxygen','replicate','week','genus'],axis=1)
    return df

def plot_chart(df,oxygen,week,replicate):
    d = Donut(df, label=['class', 'order'], values='abundance',
          text_font_size='8pt', hover_text='abundance')
    output_file("donut.html", title=oxygen + "." + str(week) + "." +str(replicate) )
    return show(d)

def disply_chart(oxygen,week,replicate):
    df1 = select_sample(oxygen,week,replicate)
    df2 = reduce_data(df1)
    plot_chart(df2,oxygen,week,replicate)
    return