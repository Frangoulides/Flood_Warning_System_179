from floodsystem import geo
from floodsystem import stationdata

set_of_stationed_rivers = geo.rivers_with_station(stationdata.build_station_list())

list_of_stationed_rivers = list(set_of_stationed_rivers)
print(sorted(list_of_stationed_rivers)[:10])