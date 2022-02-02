from floodsystem import stationdata
from floodsystem import geo
from floodsystem import utils


def closest_10(p):
    """
    Prints a list of 10 tuples containing the name of station, town and distance from
    the given coordinate in km, for the 10 closest stations to the given coordinates.
    The tuples are in ascending order according to their distance to the coordinates given.

    The coordinate shall be given as a tuple p = (latitude, longitude)

    """
    print('\n 10 stations closest to ' + str(p) + '  : \n ' )

    stations = stationdata.build_station_list()
    station_distance_list = geo.stations_by_distance(stations, p)

    temp = []
    for i in range(10):
        temp.append((station_distance_list[i][0].name, station_distance_list[i][0].town, station_distance_list[i][1]))

    print(utils.sorted_by_key(temp, 2))


def furthest_10(p):
    """
      Prints a list of 10 tuples containing the name of station, town and distance from
      the given coordinate in km, for the 10 furthest stations from the given coordinates.
      The tuples are in ascending order according to their distance to the coordinates given.

      The coordinate shall be given as a tuple p = (latitude, longitude)
      """
    print('\n 10 stations furthest from ' + str(p) + '  : \n ')

    stations = stationdata.build_station_list()
    station_distance_list = geo.stations_by_distance(stations, p)

    temp = []
    for i in range(1, 11):
        temp.append((station_distance_list[-i][0].name, station_distance_list[-i][0].town, station_distance_list[-i][1]))

    print(utils.sorted_by_key(temp, 2))


closest_10((52.2053, 0.1218))
furthest_10((52.2053, 0.1218))
