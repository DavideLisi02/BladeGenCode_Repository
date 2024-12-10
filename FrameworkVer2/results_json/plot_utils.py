
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.colors import LogNorm
from scipy.interpolate import griddata
import matplotlib
import json

matplotlib.rc('font', **{"size": 25})
plt.rcParams["figure.figsize"] = (20, 20)


def read_json_file(file_path):
    """
    Reads a JSON file and returns its content as a dictionary.
    
    :param file_path: Path to the JSON file.
    :return: Dictionary containing the JSON file content.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def plot_2d(results, labels, feature, n_data=300, log=False, cmap=None):
    """Plot result

    results - The results are given as a 2d array of dimensions [N, 3].

    labels - The labels should be a list of three string for the xlabel, the
    ylabel and zlabel (in that order).

    n_data - Represents the number of points used along x and y to draw the plot

    log - Set log to True for logarithmic scale.

    cmap - You can set the color palette with cmap. For example,
    set cmap='nipy_spectral' for high constrast results.

    """
    xnew = np.linspace(min(results[:, 0]), max(results[:, 0]), n_data)
    ynew = np.linspace(min(results[:, 1]), max(results[:, 1]), n_data)
    grid_x, grid_y = np.meshgrid(xnew, ynew)
    results_interp = griddata(
        (results[:, 0], results[:, 1]), results[:, 2],
        (grid_x, grid_y),
        method='linear',  # nearest, cubic
    )
    extent = (
        min(xnew), max(xnew),
        min(ynew), max(ynew)
    )
    if feature == "Pressure_Ratio":
        # plt.plot(results[:, 0], results[:, 1], 'r.')
        imgplot = plt.imshow(
            results_interp,
            extent=extent,
            aspect='auto',
            origin='lower',
            interpolation='none',
            vmin = 1.92,
            vmax = 1.97,
            norm=LogNorm() if log else None
        )
    else:
        # plt.plot(results[:, 0], results[:, 1], 'r.')
        imgplot = plt.imshow(
            results_interp,
            extent=extent,
            aspect='auto',
            origin='lower',
            interpolation='none',
            norm=LogNorm() if log else None
        )

    if cmap is not None:
        imgplot.set_cmap(cmap)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    cbar = plt.colorbar()
    cbar.set_label(labels[2])

