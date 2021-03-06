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

    fig = plt.figure()
    poly, date_shift = polyfit(dates, levels, p)
    y = levels

    plt.plot(dates, y, label='Measured water levels')

    x1 = np.linspace(date_shift[0], date_shift[1], 30)
    plt.plot(x1, poly(x1 - date_shift[0]), label='Best-fit polynomial of degree %s' % p)

    plt.xticks(rotation=45)
    plt.title('%s' % station.name)
    plt.legend()
    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.tight_layout()

    return fig


def plot_flow(station, dates, levels):
    """
    Plots flow data for a station
    """
    plt.plot(dates, levels)

    plt.xlabel('date')
    plt.ylabel('flow (m3/s)')
    plt.xticks(rotation=45)
    plt.title(station.name)
    plt.axhline(y=station.typical_range[0], markersize=10, linestyle='dashed')
    plt.axhline(y=station.typical_range[1], markersize=8, linestyle='dashed')

    plt.tight_layout()

    plt.show()


