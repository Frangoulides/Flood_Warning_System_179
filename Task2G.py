from floodsystem import plot
from floodsystem import datafetcher
import datetime
from floodsystem.stationdata import build_station_list
from floodsystem.geo import stations_by_catchment



if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System *** Flash Flood Warning")
    stations = build_station_list()
    print(stations_by_catchment(stations))