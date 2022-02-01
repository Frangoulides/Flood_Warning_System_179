from floodsystem import stationdata
from floodsystem import geo

stations = stationdata.build_station_list()
list_of_tupples = geo.stations_by_distance(stations, (52.2053, 0.1218))
for i in range(10):
    print((list_of_tupples[i][0].name, list_of_tupples[i][0].town, list_of_tupples[i][1]))
