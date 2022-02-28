import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np


def polyfit(dates, levels, p):
    """
    Given the water level time history (dates, levels) for a station,
    Computes a least-squares fit of a polynomial of degree p to water level data.
    Returns a tuple of the polynomial object and any shift of the time (date) axis.
    """

    x = sorted(list(matplotlib.dates.date2num(dates)), reverse=True)
    y = levels

    date_shift = (x[0], x[-1])

    p_coeff = np.polyfit(x - date_shift[0], y, p)

    poly = np.poly1d(p_coeff)

    return poly, date_shift


def running_difference(dates, levels, p):
    """
    Given dates and levels over n days, computes a running difference between the polyfit line of degree p and the
    actual data.
    """

    poly, date_shift = polyfit(dates, levels, p)
    x1 = np.linspace(date_shift[0], date_shift[1], len(levels))

    result = [a - b for a, b in zip(levels, poly(x1 - date_shift[0]).tolist())]

    return result
