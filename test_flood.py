from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.stationdata import build_station_list


def test_stations_level_over_threshold():
    stations = build_station_list()
    data = stations_level_over_threshold(stations, 0.8)
    for i in range(1, len(data)-1):
        assert data[i][1] >= data[i+1][1]

    for i in data:
        assert i[1] > 0.8


def test_stations_highest_rel_level():
    stations = build_station_list()
    output_stations = stations_highest_rel_level(stations, 10)
    assert len(output_stations) == 10

    relative_water_levels = []
    for station in output_stations:
        relative_water_levels.append(station.relative_water_level())
    for i in range(0, len(relative_water_levels)-1):
        assert relative_water_levels[i] > relative_water_levels[i+1]

