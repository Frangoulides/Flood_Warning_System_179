from floodsystem.geo import rivers_by_station_number
from floodsystem.stationdata import build_station_list


def run(N):
    """
    Prints the list of (river, number stations) tuples when N = 9.
    """
    stations = build_station_list()
    print(rivers_by_station_number(stations, N))


if __name__ == "__main__":
    print("*** Task 1E: CUED Part IA Flood Warning System ***")
    # For this task, we want N = 9
    run(9)
