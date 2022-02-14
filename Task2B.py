from floodsystem import flood, stationdata

stations = stationdata.build_station_list()

data = flood.stations_level_over_threshold(stations, 0.8)

print("*** Task 1C: CUED Part IA Flood Warning System *** \n")
for i in data:
    print(i[0].name, i[1])
