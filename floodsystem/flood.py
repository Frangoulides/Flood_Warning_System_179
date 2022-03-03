import matplotlib.pyplot as plt
from floodsystem.stationdata import update_water_levels, update_flow, build_station_list, build_flow_station_list
from floodsystem.datafetcher import fetch_measure_levels, fetch_latest_water_level_data
import datetime
from floodsystem.analysis import polyfit, polyfit_water_level_forecast
import numpy as np
from floodsystem.geo import stations_by_catchment, stations_by_river


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


def rivers_over_threshold(stations, proportion, tol):
    """
    Returns a list of rivers with a proportion of its stations over a threshhold

    """
    a = []
    update_water_levels(stations)

    for station in stations:
        if station.relative_water_level() is None or station.relative_water_level() < tol:
            pass
        else:
            a.append(station.river)

    output = []
    for b in a:
        if a.count(b) >= (proportion * len(stations_by_river(stations)[b])):
            output.append(b)

    return output


def flood_assessment(station, catchments_over_threshold_list, rivers_over_threshold_list):
    """
    Given a station object, returns a string describing the flood-risk assessment
    Flood risk is rated from a scale of 'No Risk', 'Low', 'Moderate', 'High' and 'Severe'
    """
    forecast, rate_of_rise = polyfit_water_level_forecast(station, 2, 6)
    rel_level = station.relative_water_level()

    flow_data = {}
    for flow_station in build_flow_station_list():
        flow_data[flow_station.river] = flow_station.latest_flow
    flood_risk_assessment = None

    if rel_level is None:
        return 'No Assessment'

    # No Risk

    # As long as the current relative water level is below 1, we can consider no risk as it is a typical water level
    # for that river.
    flood_risk_assessment = 'No Risk'

    # Low

    # Once the relative water level breaks through above 1, there is a low risk of flooding. This also includes
    # cases where the water level slowly creeps past the upper typical range, and thus no sharp rise means low risk
    # of flooding.
    if rel_level >= 1 and rate_of_rise <= 0.1:
        flood_risk_assessment = 'Low'

    # Moderate

    # The relative water level is half as great as the typical range, indicating an increased likelihood the water level
    # will reach the height of the river bank.
    # Also involves the catchment area to look for downstream flooding. If a catchment is recording high levels of water
    # level it is likely this will cause a domino effect both downstream and upstream:
    # This also applies to up and down a river.
    # Downstream Flooding caused by discharge recorded from upstream stations
    # Up-stream flooding caused by rising tides.

    if (rel_level >= 1.5 and forecast == 'Rising') or (station.catchment in catchments_over_threshold_list) \
            or (station.river in rivers_over_threshold_list):
        flood_risk_assessment = 'Moderate'

    # High

    # A high chance of flooding will be indicated by a high rate of water level increase on top of already high levels.
    # This is especially the case for flash flooding.
    if (rel_level >= 2 and forecast == 'Rising' and rate_of_rise >= 1) \
            or ((station.catchment in catchments_over_threshold_list) and rel_level >= 1) \
            or ((station.river in rivers_over_threshold_list) and rel_level >= 2):
        flood_risk_assessment = 'High'

    # Severe

    # When water levels are twice as high as they usually are and is somehow still rising, the flood likelihood is
    # severe.
    # Also, if the river is in a catchment area of high levels and is recording high levels itself, it can indicate
    # that levels are about to rise more (due to discharge from upstream or rising tides).

    if (rel_level >= 3 and forecast == 'Rising' and rate_of_rise >= 2) \
            or ((station.catchment in catchments_over_threshold_list) and rel_level >= 3 \
                and station.river in rivers_over_threshold_list):
        flood_risk_assessment = 'Severe'

    return flood_risk_assessment


def at_risk_towns(stations):
    """
    Given a list of stations, Returns a dictionary of towns and their risk level.
    """
    catchments = catchments_over_threshold(build_station_list(), 0.5, 1)
    rivers = rivers_over_threshold(build_station_list(), 0.5, 1)
    assessments = {'No Risk': [],
                   'Low': [],
                   'Moderate': [],
                   'High': [],
                   'Severe': [],
                   'No Assessment': []
                   }
    for station in stations:
        if station.town is not None:
            assessments[flood_assessment(station, catchments, rivers)].append(station.town)

    return assessments
