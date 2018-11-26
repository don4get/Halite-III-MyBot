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

# Fill in most of layout
layout = go.Layout(
    xaxis=dict(
       range=[0, width],
       showgrid=False,
       zeroline=False,
       showline=False,
       title='width',
       gridcolor='#bdbdbd',
       gridwidth=2,
    ),
    yaxis=dict(
        range=[0, height],
        showgrid=False,
        zeroline=False,
        showline=False,
        title='height',
        scaleanchor="x",
        scaleratio=1
    ),
    hovermode='closest',
    plot_bgcolor='rgb(223, 232, 243)'
)

figure = {
    'data': [],
    'layout': layout,
    'frames': [],
    'config': {'scrollzoom': True}
}

# Add sliders
figure['layout']['sliders'] = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'text-before-value-on-display',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': [...]
}


# Slider dictionary


plot(fig, filename='halite-map.html')