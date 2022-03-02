from floodsystem.plot import *
from floodsystem.analysis import polyfit_water_level_forecast
from floodsystem.datafetcher import fetch_measure_levels, fetch_station_flow_data, fetch_latest_flow_data
import datetime
from floodsystem.stationdata import build_station_list, build_flow_station_list, update_flow
import matplotlib.pyplot as plt
from floodsystem.flood import *


def catchment_flood(s, proportion, tol):
    print("*** Catchment Flood ***")
    print("""
    A catchment is defined as an area that water is collected by a natural landscape.
    It involves any sources, the main drain (river mouth to sea for example) and any water systems in between.
    Therefore if there is a large water input into a catchment, multiple stations will detect it.
        """)
    print("Catchments with multiple stations over max typical range:", catchments_over_threshold(s, proportion, tol))


def stations_with_rising_levels(s, n, p):
    for station in s:
        print(station.name, polyfit_water_level_forecast(station,n,p), station.relative_water_level())


def towns_at_risk(stations):
    towns = at_risk_towns(stations)
    for t in towns:
        if len(towns[t]) == 0:
            print(t, ": None")
        else:
            print(t, ":", towns[t])


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    stations = build_station_list()
    stations2 = stations_highest_rel_level(stations, 10)
    towns_at_risk(stations2)


