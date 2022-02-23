import matplotlib.dates
import matplotlib.pyplot as plt


def polyfit(dates, levels):
    """
    Given the water level time history (dates, levels) for a station,
    Computes a least-squares fit of a polynomial of degree p to water level data.
    Returns a tuple of the polynomial object and any shift of the time (date) axis.
    """

    x = list(matplotlib.dates.date2num(dates))
    y = levels

    plt.plot(x,y,".")

    return plt.show()