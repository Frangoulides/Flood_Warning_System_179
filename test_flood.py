from floodsystem.flood import stations_level_over_threshold
from floodsystem.stationdata import build_station_list


def test_stations_level_over_threshold():
    stations = build_station_list()
    data = stations_level_over_threshold(stations, 0.8)
    for i in range(1, len(data)-1):
        assert data[i][1] >= data[i+1][1]

    for i in data:
        assert i[1] > 0.8

