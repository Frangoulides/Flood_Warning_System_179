from floodsystem.plot import plot_water_levels
from floodsystem.stationdata import build_station_list
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.plot import plot_water_level_with_fit
import datetime
import matplotlib.pyplot as plt


def test_plot_water_levels():
    station = build_station_list()[0]
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=10))
    plot_water_levels(station, dates, levels)


def test_plot_water_level_with_fit():
    station = build_station_list()[0]
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=10))
    plot_water_level_with_fit(station, dates, levels, 4)
    plt.show()