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
    print(at_risk_towns(stations))


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    stations = build_station_list()
    stations2 = stations_highest_rel_level(stations, 10)
    flow_stations = build_flow_station_list()
    # catchments_over_threshold_list = catchments_over_threshold(stations, 0.5, 1)
    catchment_flood(stations, 0.5, 1)
    stations_with_rising_levels(stations2, 2, 4)
    towns_at_risk(stations2)


