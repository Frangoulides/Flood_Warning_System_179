from floodsystem.analysis import polyfit, polyfit_water_level_forecast
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list
import matplotlib.dates
import numpy as np
import datetime


def test_polyfit():
    station = build_station_list()[0]
    dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=10))
    poly, date_shift = polyfit(dates, levels, 4)

    assert poly is not None
    assert date_shift is not None


def test_polyfit_forecast():
    station = build_station_list()[0]
    forecast, rate = polyfit_water_level_forecast(station,2,2)

    assert forecast == 'Rising' or 'Falling' or None
    assert 25 > rate > -25
