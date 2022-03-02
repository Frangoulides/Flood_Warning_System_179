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


def stations_with_level_spike(s, n, p, tol):
    print("*** Stations with a sudden water level spike ***")
    print("""
    By comparing the measured water levels and its line of best fit over time, we can identify unexpected jumps.
    In order to get a good line of best fit, the data used should be over as long amount of time as possible
    relative to the time-frame. Flash-flooding takes place in the order of days, while downstream flooding
    can occur in the order of weeks. 
    """)
    print("Stations with sudden water level spikes:", spike_from_polyfit(s, n, p, tol))
    for station in spike_from_polyfit(s, n, p, tol)[0]:
        dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=n))
        plot_water_level_with_fit(station, dates, levels, p)
        plt.show()


def stations_with_rising_levels(s, n, p):
    for station in s:
        print(station.name, polyfit_water_level_forecast(station,n,p))


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    stations = build_station_list()
    stations2 = stations_highest_rel_level(stations, 5)
    flow_stations = build_flow_station_list()
    # catchment_flood(stations, 0.1, 1)
    # stations_with_level_spike(stations2, 10, 4, 2)
    # stations_with_rising_levels(stations2, 2, 4)
    for station in stations2:
        print(flood_assessment(station))
