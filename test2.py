import plotly.graph_objects as go

data = [
    dict(
        header=dict(values=['Merged Cell 1', 'Merged Cell 2', 'Cell 3']),
        cells=dict(values=[['Content', '', ''], ['', 'Content', ''], ['Content', 'Content', '']])
    )
]

layout = go.Layout(
    title='Merged Cells in Table',
    margin=dict(l=0, r=0, t=50, b=0)
)

fig = go.Figure(data=[go.Table(header=data[0]['header'], cells=data[0]['cells'])], layout=layout)
fig.show()
