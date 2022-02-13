from floodsystem.stationdata import update_water_levels


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
        else:
            output.append((station, station.relative_water_level()))

    output.sort(key=lambda x: x[1], reverse=True)
    return output
