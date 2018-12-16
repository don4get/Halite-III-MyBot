from plotly.offline import plot
import plotly.graph_objs as go
from plotly.grid_objs import Grid, Column
import numpy as np

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
    if i>4 and i<4+width:
        map.append([int(num) for num in line.split()])

file.close()


# Draw map
trace = go.Heatmap(z=map)
data = [trace]

fig = go.Figure(data=data)
plot(fig, filename='halite-map.html')
