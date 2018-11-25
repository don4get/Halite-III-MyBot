from plotly.offline import plot
import plotly.graph_objs as go

# Open file and read the map
file = open('replays/20181124-155646+0100-1543071405-32-32.txt')

map = []
width = 0
height = 0
for i, line in enumerate(file):
    if i == 4:
        size = [int(num) for num in line.split()]
        width = size[0]
        height = size[1]
        print(width)
        print(height)
    if i>4 and i<4+width:
        map.append([int(num) for num in line.split()])

file.close()


# Draw map
trace = go.Heatmap(z = map)
data=[trace]
layout = go.Layout(
    xaxis=dict(
       range=[0, width],
       showgrid=False,
       zeroline=False,
       showline=False,
       gridcolor='#bdbdbd',
       gridwidth=2,
       zerolinecolor='#969696',
       zerolinewidth=4,
       linecolor='#636363',
       linewidth=6
    ),
    yaxis=dict(
        range=[0, height],
        showgrid=False,
        zeroline=False,
        showline=False,
        scaleanchor="x",
        scaleratio=1
    )
)
fig = go.Figure(data=data, layout=layout)
plot(fig, filename='halite-map.html')