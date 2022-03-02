import matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import datetime
from floodsystem.datafetcher import fetch_measure_levels


def polyfit(dates, levels, p):
    """
    Given the water level time history (dates, levels) for a station,
    Computes a least-squares fit of a polynomial of degree p to water level data.
    Returns a tuple of the polynomial object and any shift of the time (date) axis.
    """
    if dates == None or len(dates) == 0 or levels == None or len(levels) == 0:
        return None, None

    x = sorted(list(matplotlib.dates.date2num(dates)), reverse=True)
    y = levels
    date_shift = (x[0], x[-1])

    p_coeff = np.polyfit(x - date_shift[0], y, p)

    poly = np.poly1d(p_coeff)

    return poly, date_shift


def polyfit_water_level_forecast(station, n, p):
    """
    Given the water level time history, this forecasts whether the water level is likely to be rising or falling.
    Returns a tuple (forecast, rate) where forecast is either rising or falling and rate is the rate at which the
    water level is predicted to rise. These are extrapolated from a polyfit line of degree p over time n
    """
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=n))
    poly, date_shift = polyfit(dates, levels, p)

    if poly == None or date_shift == None:
        return None, None

    d = np.polyder(poly)
    if np.polyval(d, (date_shift[1])) > 0:
        forecast = 'Rising'
    else:
        forecast = 'Falling'

    return forecast, np.polyval(d, (date_shift[1] - date_shift[0]))


