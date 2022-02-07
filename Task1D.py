from floodsystem import geo
from floodsystem import stationdata

set_of_stationed_rivers = geo.rivers_with_station(stationdata.build_station_list())

list_of_stationed_rivers = list(set_of_stationed_rivers)
if __name__ == "__main__":
    print("*** Task 1D: CUED Part IA Flood Warning System ***\n")
print('There are ' + str(len(list_of_stationed_rivers)) + ' rivers which have at least one monitoring station.\nThe'
                                                          'first 10 rivers by alphabetical order are listed below: ')
print(sorted(list_of_stationed_rivers)[:10])


def stations_in_river(river):
    """
    Returns the names of the stations located on
    the inputed river 'river' in alphabetical order.
    'river' object is a string

    """
    dictionary = geo.stations_by_river(stationdata.build_station_list())
    names = []
    for station in dictionary[river]:
        names.append(station.name)

    return sorted(names)


print('\nStations on River Aire: ')
print(stations_in_river('River Aire'))
print('\nStations on River Cam: ')
print(stations_in_river('River Cam'))
print('\nStations on River Thames: ')
print(stations_in_river('River Thames'))
