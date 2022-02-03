# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from floodsystem import utils  # noqa
from haversine import haversine


def stations_by_distance(stations, p):
    """
     Given a list of station objects and a coordinate p, returns a list of (station, distance) tuples,
     where distance (float) is the distance of the station from the coordinate p in km.
     The list is sorted by distance in ascending order.

     The coordinate shall be given as a tuple p = (latitude, longitude)

     Documentation for object 'MonitoringStation' can be found by importing 'station' from 'floodsystem'
     and typing 'help(station.MonitoringStation)'

    """

    list_of_tuples = []

    for station in stations:
        distance = haversine(station.coord, p)
        list_of_tuples.append((station, distance))

    return utils.sorted_by_key(list_of_tuples, 1)


def stations_within_radius(stations, centre, r):
    """

    Returns a list of all stations within radius r from the centre.

    stations_within_radius(stations, centre, r)

    'stations' is a list of 'MonitoringStation' objects. Documentation for object 'station' can be found
    by importing 'station' from 'floodsystem' and typing 'help(station.MonitoringStation)'

    'centre' = (latitude, longitude)         'r' = radius in km


    """
    list_of_stations = []

    for station in stations:
        radius = haversine(station.coord, centre)
        if radius < r:
            list_of_stations.append(station)
        else:
            pass

    return list_of_stations


def rivers_with_station(stations):
    """
    Returns a set of all rivers monitored by 'stations'.
    'stations' is a list of 'MonitoringStation' objects. Documentation for object 'station' can be found
    by importing 'station' from 'floodsystem' and typing 'help(station.MonitoringStation)'

    """

    river_list = []
    for station in stations:
        river_list.append(station.river)

    return set(river_list)


def stations_by_river(stations):

    """
    Returns a dictionary that maps river names (the ‘key’)
    to a list of station objects on a given river.

    'stations' is a list of 'MonitoringStation' objects. Documentation for object 'station' can be found
    by importing 'station' from 'floodsystem' and typing 'help(station.MonitoringStation)'

    """

    dictionary = {}
    for river in rivers_with_station(stations):
        river_stations = []
        for station in stations:
            if station.river == river:
                river_stations.append(station)
        dictionary.update({river: river_stations})

    return dictionary
