import __init__
import pandas as pd
import plotly
from plotly import graph_objs
import load_dataframe as data
df=data.getTokenizedDataFrame()

plotly.offline.init_notebook_mode()

proactivo = len(df[(df["proactivo"] > 0.0) | (df["proactivo.1"] > 0.0) | (df["proactivo.2"] > 0.0)])
agresivo = len(df[(df["agresivo"] > 0.0) | (df["agresivo.1"] > 0.0) | (df["agresivo.2"] > 0.0)])
provoto = len(df[(df["provoto"] > 0.0) | (df["provoto.1"] > 0.0) | (df["provoto.2"] > 0.0)])
reactivo = len(df[(df["reactivo"] > 0.0) | (df["reactivo.1"] > 0.0) | (df["reactivo.2"] > 0.0)])

totalClassified=len(df[(df["proactivo"] > 0.0) | (df["proactivo.1"] > 0.0) | (df["proactivo.2"] > 0.0) | (df["agresivo"] > 0.0) | (df["agresivo.1"] > 0.0) | (df["agresivo.2"] > 0.0) | (df["provoto"] > 0.0) | (df["provoto.1"] > 0.0) | (df["provoto.2"] > 0.0) | (df["reactivo"] > 0.0) | (df["reactivo.1"] > 0.0) | (df["reactivo.2"] > 0.0)])

print(totalClassified)

dist = [
    graph_objs.Bar(
        x=["proactivo","agresivo","provoto", "reactivo"],
        y=[proactivo, agresivo, provoto, reactivo],
)]

# plotly.offline.iplot({"data":dist, "layout":graph_objs.Layout(title="Sentiment type distribution in training set")})

plotly.offline.plot(dist, filename='images/categories-distribution.html')
