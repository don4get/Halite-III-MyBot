from plotly.offline import plot
import plotly.graph_objs as go
from plotly.grid_objs import Grid, Column
import numpy as np

# Open file and read the map
file = open('maps/replay-20181124-135752+0100-1543064270-32-32.csv')
maps = []

for i, line in enumerate(file):
    if i == 0:
        width = float(line)
    elif i == 1:
        height = float(line)
    else:
        maps.append([float(num) for num in line.split(",")])
print(maps)
maps = np.reshape(maps, (400, int(height), int(width)))

file.close()

iters = np.arange(0, 400)


# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# fill in most of layout
figure['layout']['xaxis'] = {'range': [0, width], 'title': 'x position'}
figure['layout']['yaxis'] = {'title': 'y position'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['sliders'] = {
    'args': [
        'transition', {
            'duration': 4000,
            'easing': 'cubic-in-out'
        }
    ],
    'initialValue': '0',
    'plotlycommand': 'animate',
    'values': iters,
    'visible': True
}

figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate',
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
        'prefix': 'Iterations:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 30, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

# make data
# year = 1952
# for continent in continents:
#     dataset_by_year = dataset[dataset['year'] == year]
#     dataset_by_year_and_cont = dataset_by_year[dataset_by_year['continent'] == continent]
#
#     data_dict = {
#         'x': list(dataset_by_year_and_cont['lifeExp']),
#         'y': list(dataset_by_year_and_cont['gdpPercap']),
#         'mode': 'markers',
#         'text': list(dataset_by_year_and_cont['country']),
#         'marker': {
#             'sizemode': 'area',
#             'sizeref': 200000,
#             'size': list(dataset_by_year_and_cont['pop'])
#         },
#         'name': continent
#     }
#     figure['data'].append(data_dict)

iteration = 0
trace = go.Heatmap(z=maps[iteration])
data = [trace]
figure['data'] = data

# make frames
for iteration in iters:
    trace = go.Heatmap(z=maps[iteration])
    data = [trace]
    frame = {'data': data, 'name': str(iteration)}

    figure['frames'].append(frame)
    slider_step = {'args': [
        [iteration],
        {'frame': {'duration': 0, 'redraw': True},
         'mode': 'immediate'}
    ],
        'label': str(iteration),
        'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

figure['layout']['sliders'] = [sliders_dict]

plot(figure, filename='halite-map.html')
