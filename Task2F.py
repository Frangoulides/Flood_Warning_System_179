from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list
from floodsystem.plot import plot_water_level_with_fit
import datetime


stations = build_station_list()

for station in stations:
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=2))
    plot_water_level_with_fit(station, dates, levels, 4)