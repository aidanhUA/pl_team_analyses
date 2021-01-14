import matplotlib.pyplot as plt
import numpy as np


def create_team_map(events, team_id, teams, event_type):
    x_list = []
    y_list = []
    for position in events:
        x_list.append(position['position']['x'])
        y_list.append(position['position']['y'])

    # Simplifying this into smaller bins (5 by 20 percentiles) creates a clearer demonstration of
    # where the team restarts their possessions
    heatmap, xedges, yedges = np.histogram2d(x_list, y_list, bins=(10, 10))
    extent = [0, 100, 0, 100]

    # Plot heatmap
    plt.clf()
    plt.ylabel('Width of Pitch')
    plt.xlabel('Length of Pitch')
    plt.title(teams.loc[teams['wyId'] == int(team_id), 'name'].values[0])
    plt.imshow(heatmap, extent=extent, aspect=0.5, alpha=0.5)
    plt.axis([0, 100, 0, 100])
    plt.savefig(f'plots/{event_type}.png')
