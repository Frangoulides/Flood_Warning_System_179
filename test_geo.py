from floodsystem import geo
from floodsystem import stationdata


def test_stations_by_distance():
    stations_list = geo.stations_by_distance(stationdata.build_station_list(), (52.2053, 0.1218))
    assert len(stations_list) == 2165
    assert stations_list[0][0].name == 'Cambridge Jesus Lock'
    assert stations_list[-1][0].name == 'Penberth'
    assert stations_list[0][1] == 0.840237595667494


def test_stations_within_radius():
    stations_list = geo.stations_within_radius(stationdata.build_station_list(), (52.2053, 0.1218), 10)
    assert len(stations_list) == 11
