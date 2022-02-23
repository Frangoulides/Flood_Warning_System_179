from floodsystem.analysis import polyfit
import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np


def plot_water_levels(station, dates, levels):

    plt.plot(dates, levels)

    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)
    plt.axhline(y=station.typical_range[0], markersize=10, linestyle='dashed')
    plt.axhline(y=station.typical_range[1], markersize=8, linestyle='dashed')

    plt.tight_layout()

    plt.show()


def plot_water_level_with_fit(station, dates, levels, p):
    """
    Plots the water level data and the best-fit polynomial.
    """

    poly, date_shift = polyfit(dates, levels, p)
    x = sorted(list(matplotlib.dates.date2num(dates)), reverse=True)
    y = levels

    plt.plot(x, y)

    x1 = np.linspace(x[0], x[-1], 30)
    plt.plot(x1, poly(x1 - date_shift))

    return plt.show()