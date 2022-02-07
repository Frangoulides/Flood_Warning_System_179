from floodsystem.station import inconsistent_typical_range_stations
from floodsystem.stationdata import build_station_list


def run():
    """
    Builds a list of all stations with inconsistent typical range data.
    Then prints a list of station names, in alphabetical order, for stations with inconsistent data.
    """
    # Builds a list of stations
    stations = build_station_list()

    # Prints all stations with inconsistent data
    faulty_stations_names = []
    for station in inconsistent_typical_range_stations(stations):
        faulty_stations_names.append(station.name)
    print(sorted(faulty_stations_names))


if __name__ == "__main__":
    print("*** Task 1F: CUED Part IA Flood Warning System ***")
    run()