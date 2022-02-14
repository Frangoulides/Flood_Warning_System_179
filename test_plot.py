from floodsystem.plot import plot_water_levels
from floodsystem.stationdata import build_station_list
from floodsystem.datafetcher import fetch_measure_levels
import datetime


def test_plot_water_levels():
    station = build_station_list()[0]
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=10))
    plot_water_levels(station, dates, levels)
