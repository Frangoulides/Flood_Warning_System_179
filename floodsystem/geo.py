# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from haversine import haversine, Unit
from stationdata import build_station_list


def stations_by_distance(stations, p):
    # stations are inputed in the form floodsystem.station.MonitoringStation(station_id, measure_id, label, coord,
    #                                                                                  typical_range, river, town)

    # p is in the form (lattitude, longitude)

    # stations = build_station_list       # this is a list of 2165 station objects; stations[-1] prints the last station
    #                                     ; stations[-1].coord prints the coordinates of the last station

    list_of_tuples = []

    for station in stations:
        distance = haversine(station.coord, p)
        list_of_tuples.append((station, distance))

    return sorted_by_key(list_of_tuples, 1)


