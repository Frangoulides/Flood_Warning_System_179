from floodsystem import geo
from floodsystem import stationdata


def test_stations_by_distance():

    station_list = stationdata.build_station_list()

    list = geo.stations_by_distance(station_list, (52.2053, 0.1218))

    assert(len(list) == 2165)
