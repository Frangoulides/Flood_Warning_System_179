# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides interface for extracting statiob data from
JSON objects fetched from the Internet and

"""

from . import datafetcher
from .station import MonitoringStation
from floodsystem.station import FlowMonitoringStation


def build_station_list(use_cache=True):
    """Build and return a list of all river level monitoring stations
    based on data fetched from the Environment agency. Each station is
    represented as a MonitoringStation object.

    The available data for some station is incomplete or not
    available.

    """

    # Fetch station data
    data = datafetcher.fetch_station_data(use_cache)

    # Build list of MonitoringStation objects
    stations = []
    for e in data["items"]:
        # Extract town string (not always available)
        town = None
        if 'town' in e:
            town = e['town']

        # Extract river name (not always available)
        river = None
        if 'riverName' in e:
            river = e['riverName']

        # Attempt to extract typical range (low, high)
        try:
            typical_range = (float(e['stageScale']['typicalRangeLow']),
                             float(e['stageScale']['typicalRangeHigh']))
        except Exception:
            typical_range = None

        catchment = None
        if 'catchmentName' in e:
            catchment = e['catchmentName']

        try:
            # Create measure station object if all required data is
            # available, and add to list
            s = MonitoringStation(
                station_id=e['@id'],
                measure_id=e['measures'][-1]['@id'],
                label=e['label'],
                coord=(float(e['lat']), float(e['long'])),
                typical_range=typical_range,
                catchment=catchment,
                river=river,
                town=town)
            stations.append(s)
        except Exception:
            # Not all required data on the station was available, so
            # skip over
            pass

    return stations


def update_water_levels(stations):
    """Attach level data contained in measure_data to stations

    Updates the latest water level for all stations in the list 'stations' using data fetched from the Internet

    """

    # Fetch level data
    measure_data = datafetcher.fetch_latest_water_level_data()

    # Build map from measure id to latest reading (value)
    measure_id_to_value = dict()
    for measure in measure_data['items']:
        if 'latestReading' in measure:
            latest_reading = measure['latestReading']
            measure_id = latest_reading['measure']
            measure_id_to_value[measure_id] = latest_reading['value']

    # Attach latest reading to station objects
    for station in stations:

        # Reset latestlevel
        station.latest_level = None

        # Atach new level data (if available)
        if station.measure_id in measure_id_to_value:
            if isinstance(measure_id_to_value[station.measure_id], float):
                station.latest_level = measure_id_to_value[station.measure_id]


def build_flow_station_list(use_cache=True):
    """Build and return a list of all flow monitoring stations
    based on data fetched from the Environment agency. Each station is
    represented as a FlowMonitoringStation object.

    The available data for some station is incomplete or not
    available.

    """

    # Fetch station data
    data = datafetcher.fetch_station_flow_data(use_cache)

    # Build list of FlowMonitoringStation objects
    stations = []
    for e in data["items"]:
        # Extract town string (not always available)
        town = None
        if 'town' in e:
            town = e['town']

        # Extract river name (not always available)
        river = None
        if 'riverName' in e:
            river = e['riverName']

        catchment = None
        if 'catchmentName' in e:
            catchment = e['catchmentName']

        # Attempt to extract typical range (low, high)
        try:
            typical_range = (float(e['stageScale']['typicalRangeLow']),
                             float(e['stageScale']['typicalRangeHigh']))
        except Exception:
            typical_range = None

        s = FlowMonitoringStation(
            measure_id=e['measures'][-1]['@id'],
            label=e['label'],
            coord=(float(e['lat']), float(e['long'])),
            typical_range=typical_range,
            catchment=catchment,
            town=town,
            river=river)
        stations.append(s)

    return stations


def update_flow(flow_stations):
    """Attach level data contained in measure_data to stations

    Updates the latest water level for all stations in the list 'stations' using data fetched from the Internet

    """

    # Fetch level data
    measure_data = datafetcher.fetch_latest_flow_data()

    # Build map from measure id to the latest reading (value)
    measure_id_to_value = dict()
    for measure in measure_data['items']:
        if 'latestReading' in measure:
            latest_reading = measure['latestReading']
            measure_id = latest_reading['measure']
            measure_id_to_value[measure_id] = latest_reading['value']

    # Attach the latest reading to flow station objects
    for station in flow_stations:

        # Reset latest level
        station.latest_flow = None

        # Attach new level data (if available)
        if station.measure_id in measure_id_to_value:
            if isinstance(measure_id_to_value[station.measure_id], float):
                station.latest_flow = measure_id_to_value[station.measure_id]