from floodsystem import stationdata
from floodsystem import geo
from floodsystem import utils


def closest_10(p):
    print('\n 10 stations closest to ' + str(p) + '  : \n ' )

    stations = stationdata.build_station_list()
    station_distance_list = geo.stations_by_distance(stations, p)

    temp = []
    for i in range(10):
        temp.append((station_distance_list[i][0].name, station_distance_list[i][0].town, station_distance_list[i][1]))

    print(utils.sorted_by_key(temp, 2))


def furthest_10(p):
    print('\n 10 stations furthest from ' + str(p) + '  : \n ')

    stations = stationdata.build_station_list()
    station_distance_list = geo.stations_by_distance(stations, p)

    temp = []
    for i in range(1, 11):
        temp.append((station_distance_list[-i][0].name, station_distance_list[-i][0].town, station_distance_list[-i][1]))

    print(utils.sorted_by_key(temp, 2))


closest_10((52.2053, 0.1218))
furthest_10((52.2053, 0.1218))