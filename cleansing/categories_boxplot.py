import __init__
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import load_dataframe
df=load_dataframe.getTokenizedDataFrame()

plotly.offline.init_notebook_mode()

dfMartha = pd.melt(df[(df["proactivo"] > 0.0) | (df["provoto"] > 0.0) | (df["agresivo"] > 0.0) | (df["reactivo"] > 0.0)], id_vars=['id'], var_name="attitude", value_name="rank", value_vars=['proactivo', 'agresivo', 'provoto', 'reactivo'])
traces = list()
for att in dfMartha.attitude.unique():
	traces.append(plotly.graph_objs.Box(y=np.array(dfMartha[(dfMartha.attitude == att) & (dfMartha['rank']>0)]['rank'].values, dtype=float), name = att, boxmean='sd', boxpoints=False))
layout = go.Layout(
    title='Non-zero--based',
    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
)
fig = go.Figure(data=traces, layout=layout)
plotly.offline.plot(fig, filename='images/martha-nozeros.html')

traces = list()
for att in dfMartha.attitude.unique():
	traces.append(plotly.graph_objs.Box(y=np.array(dfMartha[(dfMartha.attitude == att)]['rank'].values, dtype=float), name = att, boxmean='sd', boxpoints=False))
layout = go.Layout(
    title='Zero-based',
    font=dict(family='Courier New, monospace', size=24, color='#7f7f7f')
)
fig = go.Figure(data=traces, layout=layout)
plotly.offline.plot(fig, filename='images/martha-zeros.html')