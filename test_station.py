# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""Unit test for the station module"""

from floodsystem.station import MonitoringStation, inconsistent_typical_range_stations
from floodsystem.stationdata import build_station_list


def test_create_monitoring_station():
    # Create a station
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "some station"
    coord = (-2.0, 4.0)
    trange = (-2.3, 3.4445)
    river = "River X"
    town = "My Town"
    s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    assert s.station_id == s_id
    assert s.measure_id == m_id
    assert s.name == label
    assert s.coord == coord
    assert s.typical_range == trange
    assert s.river == river
    assert s.town == town


def test_inconsistent_typical_range_stations():
    """
    Tests the inconsistent_typical_range_consistent() function within the station module

    Also, since applicable, typical_range_consistent() function within submodule MonitoringStation will also be tested here.
    """
    stations = build_station_list()
    # Create test station with trange = None
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "station s"
    coord = (-2.0, 4.0)
    trange = None
    river = "River Y"
    town = "My City"
    s = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    # Create test station with trange = (q,p) where q > p
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "station t"
    coord = (-2.0, 4.0)
    trange = (4, 1)
    river = "River Y"
    town = "My City"
    t = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    # Create test station with a consistent t_range
    s_id = "test-s-id"
    m_id = "test-m-id"
    label = "station u"
    coord = (-2.0, 4.0)
    trange = (1, 3)
    river = "River Y"
    town = "My City"
    u = MonitoringStation(s_id, m_id, label, coord, trange, river, town)

    stations.append(t)
    stations.append(s)
    stations.append(u)

    # inconsistent_typical_range_stations() test
    assert s in inconsistent_typical_range_stations(stations)
    assert t in inconsistent_typical_range_stations(stations)
    assert u not in inconsistent_typical_range_stations(stations)

    # typical_range_consistent() test
    assert MonitoringStation.typical_range_consistent(s) is False
    assert MonitoringStation.typical_range_consistent(t) is False
    assert MonitoringStation.typical_range_consistent(u) is True
