from floodsystem.stationdata import update_water_levels


def stations_level_over_threshold(stations, tol):
    """
    Returns a list of (station, relative water level) tuples in descending relative water level,
    for all stations with a relative water level bigger than tol.

    """
    output = []
    update_water_levels(stations)

    for station in stations:
        if station.typical_range_consistent:
            if station.relative_water_level > tol:
                output.append((station, station.relative_water_level))

    return output.sort(key=lambda x: x[1])
