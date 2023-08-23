import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Example data (replace these lists with your actual data)
list_names = ['List 1', 'List 2', 'List 3', 'List 4', 'List 5']
list_values = [
    [22.91, 47.9, 3.33, 10.28, 15.58],
    [4.05, 85.51, 0.18, 0.09, 10.17],
    [10.18, 32.44, 3.9, 17.36, 36.12],
    [6.57, 84.43, 0.36, 0.99, 7.66],
    [6.57, 84.43, 0.36, 0.99, 7.66]
]

# Create subplots
fig = make_subplots(rows=1, cols=len(list_names), shared_yaxes=True)

for i, name in enumerate(list_names, start=1):
    df = pd.DataFrame({'Value': list_values[i - 1]})
    fig.add_trace(go.Box(x=df['Value'], name=name, showlegend=False), row=1, col=i)

# Update layout
fig.update_layout(title='Subplots with Swarm Plots',
                  xaxis_title='Value',
                  yaxis_title='List Name')

# Show the plot
fig.show()
