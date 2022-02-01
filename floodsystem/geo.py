# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
from haversine import haversine


def stations_by_distance(stations, p):
    """
     Given a list of station objects and a coordinate p, returns a list of (station, distance) tuples,
     where distance (float) is the distance of the station from the coordinate p in km.
     The list is sorted by distance in ascending order.

     The coordinate shall be given as a tuple p = (latitude, longitude)

     Documentation for object 'station' can be found by importing 'station' from 'floodsystem'
     and typing 'help(station.MonitoringStation)'

    """

    list_of_tuples = []

    for station in stations:
        distance = haversine(station.coord, p)
        list_of_tuples.append((station, distance))

    return sorted_by_key(list_of_tuples, 1)


