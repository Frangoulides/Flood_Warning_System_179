import matplotlib.pyplot as plt
from floodsystem.stationdata import update_water_levels, update_flow, build_station_list
from floodsystem.datafetcher import fetch_measure_levels, fetch_latest_water_level_data
import datetime
from floodsystem.analysis import polyfit, polyfit_water_level_forecast
import numpy as np
from floodsystem.geo import stations_by_catchment


def stations_level_over_threshold(stations, tol):
    """
    Returns a list of (station, relative water level) tuples in descending relative water level,
    for all stations with a relative water level bigger than tol.
    It also checks if the station.typical_range is a valid entry before proceeding.

    """
    output = []
    update_water_levels(stations)

    for station in stations:
        if station.relative_water_level() is None or station.relative_water_level() < tol:
            pass
        elif station.relative_water_level() > 20:
            print(
                'Station ' + station.name + ' was excluded because the relative water level value is unrealistic. Value: ' + str(
                    station.relative_water_level()))
        else:
            output.append((station, station.relative_water_level()))

    output.sort(key=lambda x: x[1], reverse=True)
    return output


def stations_highest_rel_level(stations, n):
    """
    Returns a list of the N stations (objects) at which the water level, relative to the typical range, is highest.
    The list is sorted in descending order by relative level.
    """

    data = stations_level_over_threshold(stations, 0)
    output_stations = []
    for i in range(n):
        output_stations.append(data[i][0])

    return output_stations


def catchments_over_threshold(stations, proportion, tol):
    """
    Returns a list of any catchments with a percentage of their stations recording water levels above a threshold
    """

    a = []
    update_water_levels(stations)

    for station in stations:
        if station.relative_water_level() is None or station.relative_water_level() < tol:
            pass
        else:
            a.append(station.catchment)

    output = []
    for b in a:
        if a.count(b) >= (proportion * len(stations_by_catchment(stations)[b])):
            output.append(b)

    return output


def flow_stations_over_threshold(stations, tol):
    """
    Returns a list of (flow_station, relative water level) tuples in descending relative flow level,
    for all stations with a relative water level bigger than tol.
    It also checks if the station.typical_range is a valid entry before proceeding.

    """
    output = []
    update_flow(stations)

    for station in stations:
        if station.relative_flow() is None or station.relative_flow() < tol:
            pass
        elif station.relative_flow() > 20:
            print(
                'Station ' + station.name + ' was excluded because the relative flow value is unrealistic. Value: ' + str(
                    station.relative_flow()))
        else:
            output.append((station, station.relative_flow()))

    output.sort(key=lambda x: x[1], reverse=True)
    return output


def spike_from_polyfit(stations, n, p, tol):
    """
    Given a list of stations, this returns a list of stations that have its latest readings that spike tol above its
    polyfit line. This polyfit line is calculated over n days and is of degree p.
    """
    result = []
    for station in stations:
        dates, levels = fetch_measure_levels(station.measure_id, dt=datetime.timedelta(days=n))
        poly, date_shift = polyfit(dates[0:(len(dates)-1)], levels[0:(len(levels)-1)], p)

        latest_polyfit_value = np.polyval(poly, (date_shift[1] - date_shift[0]))
        if (levels[-1]/latest_polyfit_value) > tol:
            result.append(station)
        else:
            pass

    return result


def flood_assessment(station):
    """
    Given a station object, returns a tuple of (station, flood risk)
    Flood risk is rated from a scale of 'No Risk', 'Low', 'Moderate', 'High' and 'Severe'
    """
    forecast, rate_of_rise = polyfit_water_level_forecast(station, 5, 4)
    rel_level = station.relative_water_level()
    stations = build_station_list()
    flood_risk_assessment = None

    # No Risk
    flood_risk_assessment = 'No Risk'

    # Low

    if rel_level >= 1:
        flood_risk_assessment = 'Low'

    # Moderate

    moderate_risk_catchments = catchments_over_threshold(stations, 0.3, 1)

    if (rel_level >= 1.5 and forecast == 'Rising') or (station.catchment in moderate_risk_catchments):
        flood_risk_assessment = 'Moderate'

    # High

    high_risk_catchment = catchments_over_threshold(stations, 0.5, 1)
    if (rel_level >= 1.5 and forecast == 'Rising' and rate_of_rise >= 0.5) or ((station in high_risk_catchment) and
                                                                               rel_level >= 1):
        flood_risk_assessment = 'High'

    # Severe
    if (rel_level >= 1.5 and forecast == 'Rising' and rate_of_rise >= 0.5) or ((station in high_risk_catchment) and
                                                                               rel_level >= 1.5):
        flood_risk_assessment = 'High'

    return station.name, flood_risk_assessment, station.river, station.town





