from floodsystem.plot import plot_water_level_with_fit
from floodsystem.stationdata import build_station_list
from floodsystem.flood import stations_highest_rel_level
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.plot import plot_running_difference
import datetime
import matplotlib.pyplot as plt
from floodsystem.flood import flash_flood_polyfit


def run_flash_flood(tol, p, n):
    """
    Plots the water level over time graph of the 5 stations with the greatest relative water levels.
    This is using data over a span of the last n days.
    Also plots a best-fit polynomial of degree p on the same axis.
    """
    stations = stations_highest_rel_level(build_station_list(), 5)
    print(flash_flood_polyfit(stations, tol, p, n))
    for station in stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=n))
        plot_running_difference(station, dates, levels, p)
        plot_water_level_with_fit(station, dates, levels, p)
        plt.axhline(y=station.typical_range[1], markersize=10, linestyle='dashed', label='typical high', color='b')
        plt.axhline(y=station.typical_range[0], markersize=10, linestyle='dashed', label='typical low', color='r')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System *** Flash Flood Warning")
    # For this we want 10 days, tol = 1.2 and degree p = 4
    run_flash_flood(0.5, 4, 5)
