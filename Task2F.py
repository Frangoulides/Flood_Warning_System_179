from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list
from floodsystem.plot import plot_water_level_with_fit
from floodsystem.flood import stations_highest_rel_level
import datetime
import matplotlib.pyplot as plt


def run(n, p):
    """
    Plots the water level over time graph of the 5 stations with the greatest relative water levels.
    This is using data over a span of the last n days.
    Also plots a best-fit polynomial of degree p on the same axis.
    """
    stations = stations_highest_rel_level(build_station_list(), 5)
    for station in stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=n))
        plot_water_level_with_fit(station, dates, levels, p)
        plt.suptitle('Typical Range: %s' % str(station.typical_range))
        plt.show()

    return None


if __name__ == "__main__":
    print("*** Task 2F: CUED Part IA Flood Warning System ***")
    # For this we want days n = 2 and degree p = 4
    run(2, 4)
