# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides functionality for retrieving real-time and
latest time history level data

"""

import datetime
import json
import os

import dateutil.parser
import requests


def fetch(url):
    """Fetch data from url and return fetched JSON object"""
    r = requests.get(url)
    data = r.json()
    return data


def dump(data, filename):
    """Save JSON object to file"""
    f = open(filename, 'w')
    data = json.dump(data, f)
    f.close()


def load(filename):
    """Load JSON object from file"""
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    return data


def fetch_station_data(use_cache=True):
    """Fetch data from Environment agency for all active river level
    monitoring stations via a REST API and return retrieved data as a
    JSON object.

    Fetched data is dumped to a cache file so on subsequent call it can
    optionally be retrieved from the cache file. This is faster than
    retrieval over the Internet and avoids excessive calls to the
    Environment Agency service.

    """

# the data from one station look like that:
    #{'@id': 'http://environment.data.gov.uk/flood-monitoring/id/stations/055027_TG_328', 'RLOIid': '2225', 'catchmentName': 'Wye', 'dateOpened': '1990-03-08', 'easting': 364065, 'gridReference': 'SO6406525717', 'label': 'Sandford Bridge', 'lat': 51.928793, 'long': -2.524006, 'measures': [{'@id': 'http://environment.data.gov.uk/flood-monitoring/id/measures/055027_TG_328-level-stage-i-15_min-mASD', 'parameter': 'level', 'parameterName': 'Water Level', 'period': 900, 'qualifier': 'Stage', 'unitName': 'mASD'}], 'northing': 225717, 'notation': '055027_TG_328', 'riverName': 'Rudhall Brook', 'stageScale': {'@id': 'http://environment.data.gov.uk/flood-monitoring/id/stations/055027_TG_328/stageScale', 'highestRecent': {'@id': 'http://environment.data.gov.uk/flood-monitoring/id/stations/055027_TG_328/stageScale/highestRecent', 'dateTime': '2012-11-25T05:45:00', 'value': 1.219}, 'maxOnRecord': {'@id': 'http://environment.data.gov.uk/flood-monitoring/id/stations/055027_TG_328/stageScale/maxOnRecord', 'dateTime': '2012-11-25T05:45:00', 'value': 1.229}, 'minOnRecord': {'@id': 'http://environment.data.gov.uk/flood-monitoring/id/stations/055027_TG_328/stageScale/minOnRecord', 'dateTime': '2006-09-13T14:00:00', 'value': 0.026}, 'scaleMax': 2, 'typicalRangeHigh': 0.313, 'typicalRangeLow': 0.075}, 'stationReference': '055027_TG 328', 'status': 'http://environment.data.gov.uk/flood-monitoring/def/core/statusActive', 'town': 'Sandford Bridge', 'wiskiID': '055027'}

    # URL for retrieving data for active stations with river level
    # monitoring (see
    # http://environment.data.gov.uk/flood-monitoring/doc/reference)
    url = "http://environment.data.gov.uk/flood-monitoring/id/stations?status=Active&parameter=level&qualifier=Stage&_view=full"  # noqa

    sub_dir = 'cache'
    try:
        os.makedirs(sub_dir)
    except FileExistsError:
        pass
    cache_file = os.path.join(sub_dir, 'station_data.json')

    # Attempt to load station data from file, otherwise fetch over
    # Internet
    if use_cache:
        try:
            # Attempt to load from file
            data = load(cache_file)
        except FileNotFoundError:
            # If load from file fails, fetch and dump to file
            data = fetch(url)
            dump(data, cache_file)
    else:
        # Fetch and dump to file
        data = fetch(url)
        dump(data, cache_file)

    return data


def fetch_latest_water_level_data(use_cache=False):
    """Fetch latest levels from all 'measures'. Returns JSON object"""

    # URL for retrieving data
    url = "http://environment.data.gov.uk/flood-monitoring/id/measures?parameter=level&qualifier=Stage&qualifier=level"  # noqa

    sub_dir = 'cache'
    try:
        os.makedirs(sub_dir)
    except FileExistsError:
        pass
    cache_file = os.path.join(sub_dir, 'level_data.json')

    # Attempt to load level data from file, otherwise fetch over
    # Internet
    if use_cache:
        try:
            # Attempt to load from file
            data = load(cache_file)
        except FileNotFoundError:
            data = fetch(url)
            dump(data, cache_file)
    else:
        data = fetch(url)
        dump(data, cache_file)

    return data


def fetch_measure_levels(measure_id, dt):
    """Fetch measure levels from latest reading and going back a period
    dt. Return list of dates and a list of values.

    """

    # Current time (UTC)
    now = datetime.datetime.utcnow()

    # Start time for data
    start = now - dt

    # Construct URL for fetching data
    url_base = measure_id
    url_options = "/readings/?_sorted&since=" + start.isoformat() + 'Z'
    url = url_base + url_options

    # Fetch data
    data = fetch(url)

    # Extract dates and levels
    dates, levels = [], []
    for measure in data['items']:
        # Convert date-time string to a datetime object
        d = dateutil.parser.parse(measure['dateTime'])

        # Append data
        dates.append(d)
        levels.append(measure['value'])

    return dates, levels
