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

trace = go.Heatmap(z = map)
data=[trace]

turns = ['0', '1', '2']

# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# fill in most of layout
figure['layout']['xaxis'] = {
    'range': [0, width],
    'showgrid': False,
    'zeroline': False,
    'showline': False,
    'gridcolor': '#bdbdbd',
    'gridwidth': 2,
    'title': 'width'
}
figure['layout']['yaxis'] = {
    'range': [0, height],
    'showgrid': False,
    'zeroline': False,
    'showline': False,
    'gridcolor': '#bdbdbd',
    'gridwidth': 2,
    'scaleanchor': "x",
    'scaleratio': 1,
    'title': 'height'
}

figure['layout']['hovermode'] = 'closest'
figure['layout']['sliders'] = {
    'args': [
        'transition', {
            'duration': 400,
            'easing': 'cubic-in-out'
        }
    ],
    'initialValue': turns[0],
    'plotlycommand': 'animate',
    'values': turns,
    'visible': True
}
figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                                'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                  'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

# make frames
for turn in turns:
    turn = int(turn)
    frame = {'data': data, 'name': str(turn)}

    figure['frames'].append(frame)
    slider_step = {'args': [
        [turn],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
         'transition': {'duration': 300}}
    ],
        'label': turn,
        'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

figure['layout']['sliders'] = [sliders_dict]

plot(figure)