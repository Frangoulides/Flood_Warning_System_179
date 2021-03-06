from floodsystem import geo
from floodsystem import stationdata
from haversine import haversine
from floodsystem.station import MonitoringStation



def test_stations_by_distance():
    stations_list = geo.stations_by_distance(stationdata.build_station_list(), (52.2053, 0.1218))

    assert stations_list[0][0].name == 'Cambridge Jesus Lock'
    assert stations_list[-1][0].name == 'Penberth'
    assert stations_list[0][1] == 0.840237595667494


def test_stations_within_radius():
    stations_list = geo.stations_within_radius(stationdata.build_station_list(), (52.2053, 0.1218), 10)
    assert len(stations_list) == 11
    for station in stations_list:
        radius = haversine(station.coord, (52.2053, 0.1218))
        assert radius < 10


def test_rivers_by_station_number():
    # Create 100 new stations on an imaginary river called 'HopefullyNotARealRiverName'.
    stations = stationdata.build_station_list()
    for i in range(100):
        s_id = "test-s-id"
        m_id = "test-m-id"
        label = "some station"
        coord = (-2.0, 4.0)
        trange = (-2.3, 3.4445)
        catchment = 'catchment'
        river = "HopefullyNotARealRiverName"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, catchment, river, town)
        stations.append(s)

    assert ("HopefullyNotARealRiverName", 100) in geo.rivers_by_station_number(stations, 5)
    assert len(geo.rivers_by_station_number(stations, 5)) >= 5


def test_catchment_with_stations():
    stations = []
    for i in range(10):
        s_id = "test-s-id"
        m_id = "test-m-id"
        label = "some station"
        coord = (-2.0, 4.0)
        trange = (-2.3, 3.4445)
        catchment = 'catchment'
        river = "HopefullyNotARealRiverName"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, catchment, river, town)
        stations.append(s)

    assert 'catchment' in geo.catchments_with_station(stations)


def test_stations_by_catchment():
    stations = stationdata.build_station_list()
    for i in range(10):
        s_id = "test-s-id"
        m_id = "test-m-id"
        label = "some station"
        coord = (-2.0, 4.0)
        trange = (-2.3, 3.4445)
        catchment = 'catchment'
        river = "HopefullyNotARealRiverName"
        town = "My Town"
        s = MonitoringStation(s_id, m_id, label, coord, trange, catchment, river, town)
        stations.append(s)

    assert len(geo.stations_by_catchment(stations)['catchment']) == 10
