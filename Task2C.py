from floodsystem import flood, stationdata

stations = stationdata.build_station_list()

output_stations = flood.stations_highest_rel_level(stations, 10)

print("*** Task 1C: CUED Part IA Flood Warning System *** \n")

for station in output_stations:
    print(station.name, station.relative_water_level())