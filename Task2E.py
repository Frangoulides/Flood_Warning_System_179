from floodsystem.datafetcher import fetch_measure_levels
import datetime
from floodsystem.flood import stations_highest_rel_level
from floodsystem.stationdata import build_station_list
from floodsystem.plot import plot_water_levels


stations = stations_highest_rel_level(build_station_list(), 5)
for station in stations:
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=10))
    plot_water_levels(station, dates, levels)
