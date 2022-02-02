from floodsystem import geo
from floodsystem import stationdata

stations = stationdata.build_station_list()

stations_within_range = geo.stations_within_radius(stations, (52.2053, 0.1218), 10)

names = []
for i in stations_within_range:
    names.append(i.name)

print(sorted(names))