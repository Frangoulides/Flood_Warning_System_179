from floodsystem import stationdata

stations = stationdata.build_station_list()

print(stations[-1].coord)