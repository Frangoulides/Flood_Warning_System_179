import matplotlib.pyplot as plt

from floodsystem.stationdata import update_water_levels
from floodsystem.datafetcher import fetch_measure_levels
import datetime
from floodsystem.analysis import polyfit
import numpy as np
from floodsystem.analysis import running_difference


def stations_level_over_threshold(stations, tol):
    """
    Returns a list of (station, relative water level) tuples in descending relative water level,
    for all stations with a relative water level bigger than tol.
    It also checks if the station.typical_range is a valid entry before proceeding.

    """
    output = []
    update_water_levels(stations)

    for station in stations:
        if station.relative_water_level() is None or station.relative_water_level() < tol:
            pass
        elif station.relative_water_level() > 20:
            print(
                'Station ' + station.name + ' was excluded because the relative water level value is unrealistic. Value: ' + str(
                    station.relative_water_level()))
        else:
            output.append((station, station.relative_water_level()))

    output.sort(key=lambda x: x[1], reverse=True)
    return output


def stations_highest_rel_level(stations, n):
    """
    Returns a list of the N stations (objects) at which the water level, relative to the typical range, is highest.
    The list is sorted in descending order by relative level.
    """

    data = stations_level_over_threshold(stations, 0)
    output_stations = []
    for i in range(n):
        output_stations.append(data[i][0])

    return output_stations


def flash_flood_polyfit(stations, tol, p, n):
    """
    Given a list of stations, this returns the stations that have positive difference increase above tol.
    To account for differences varying across stations (and therefore a need for a varying tol), we take the compare the
    current difference and that stations typical-range. Now we define tol as the max ratio of current difference
    and typical range.


    """

    result = []
    test = []
    for station in stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=n))
        d = running_difference(dates, levels, p)
        test.append(d[-1] / (station.typical_range[0] - station.typical_range[1]))
        if d[-1] / (station.typical_range[0] - station.typical_range[1]) > tol:
            result.append(station)

    return result, test
