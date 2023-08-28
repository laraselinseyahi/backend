import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Sample data
data = [
    [1, 2, 3, 4],
    [2, 3, 4, 5],
    [3, 4, 5, 6]
]

# Sample variable names
variable_names = ["Variable A", "Variable B", "Variable C"]

colors = ['blue', 'green', 'red']  # Colors corresponding to each variable

fig = make_subplots(rows=1, cols=3)

for i, values in enumerate(data):
    color = colors[i]
    
    # Create a scatter trace for individual data points
    scatter_trace = go.Scatter(
        x=[variable_names[i]] * len(values),
        y=values,
        mode='markers',
        name=variable_names[i],
        marker=dict(color=color),  # Set the color of the dots
        hoverinfo='y+name+x'
    )
    
    # Create a box trace for the box plot
    box_trace = go.Box(y=values, name=variable_names[i], marker=dict(color=color), hoverinfo='y+name')
    
    fig.add_trace(scatter_trace, row=1, col=i+1)
    fig.add_trace(box_trace, row=1, col=i+1)

fig.update_layout(showlegend=False)  # To avoid duplicate legends
fig.show()


