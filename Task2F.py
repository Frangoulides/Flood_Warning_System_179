from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list
from floodsystem.analysis import polyfit
import datetime


stations = build_station_list()

for station in stations:
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=10))
    polyfit(dates,levels)