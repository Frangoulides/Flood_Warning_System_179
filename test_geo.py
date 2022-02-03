from floodsystem import geo
from floodsystem import stationdata
from haversine import haversine


def test_stations_by_distance():
    """
    Tests if the name of the first and last stations is correct.
    Checks if the coordinates of the first station is correct.
    """
    stations_list = geo.stations_by_distance(stationdata.build_station_list(), (52.2053, 0.1218))

    assert stations_list[0][0].name == 'Cambridge Jesus Lock'
    assert stations_list[-1][0].name == 'Penberth'
    assert stations_list[0][1] == 0.840237595667494


def test_stations_within_radius():
    """
    Checks if the radius is less than the specified
    """
    stations_list = geo.stations_within_radius(stationdata.build_station_list(), (52.2053, 0.1218), 10)
    assert len(stations_list) == 11
    for station in stations_list:
        radius = haversine(station.coord, (52.2053, 0.1218))
        assert radius < 10


def test_rivers_with_station():
    """
    Checks if there are duplicates of any river
    """
    rivers = geo.rivers_with_station(stationdata.build_station_list())
    rivers_list = list(rivers)
    for river in rivers_list:
        assert river in rivers_list.pop(rivers_list.index(river))


def test_stations_by_river():
    """
    Checks if all rivers and all stations are included
    """
    dictionary = geo.stations_by_river(stationdata.build_station_list())

    assert len(dictionary) == len(geo.rivers_with_station(stationdata.build_station_list()))

    n = 0
    for i in dictionary.values():
        for j in i:
            n += 1

    assert n == len(stationdata.build_station_list())
