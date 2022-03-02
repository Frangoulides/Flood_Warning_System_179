# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module provides a model for a monitoring station, and tools
for manipulating/modifying station data

"""


class MonitoringStation:
    """This class represents a river monitoring station"""

    def __init__(self, station_id, measure_id, label, coord, typical_range, catchment,
                 river, town):
        self.station_id = station_id
        self.measure_id = measure_id

        # Handle case of erroneous data where data system returns
        # '[label, label]' rather than 'label'
        self.name = label
        if isinstance(label, list):
            self.name = label[0]

        self.coord = coord
        self.typical_range = typical_range
        self.river = river
        self.town = town
        self.catchment = catchment
        self.latest_level = None

    def __repr__(self):
        d = "Station name:         {}\n".format(self.name)
        d += "   id:                {}\n".format(self.station_id)
        d += "   measure id:        {}\n".format(self.measure_id)
        d += "   coordinate:        {}\n".format(self.coord)
        d += "   town:              {}\n".format(self.town)
        d += "   river:             {}\n".format(self.river)
        d += "   typical range:     {}".format(self.typical_range)
        d += "   catchment:         {}\n".format(self.catchment)
        return d

    def typical_range_consistent(self):
        """
        Checks the typical high/low range data for consistency.
        The method should return True if the data is consistent and False if the data is inconsistent or unavailable.
        Consistency is defined as when the typical high range is larger than the typical low range
        """
        if self.typical_range is None or len(self.typical_range) != 2:
            return False
        elif self.typical_range[0] > self.typical_range[1]:
            return False
        elif self.typical_range[0] is None or self.typical_range[1] is None:
            return False
        else:
            return True

    def relative_water_level(self):
        """
        Returns the latest water level as a fraction of the typical range.
        i.e. a ratio of 1.0 corresponds to a level at the typical high and
        a ratio of 0.0 corresponds to a level at the typical low.

        """
        if self.typical_range_consistent() is True and self.latest_level is not None:   # i.e. if the typical range is correctly presented
            return (self.latest_level - self.typical_range[0])/(self.typical_range[1] - self.typical_range[0])
        else:
            return None


def inconsistent_typical_range_stations(stations):
    """
    Given a list of station objects, returns a list of stations that have inconsistent data.
    """
    inconsistent_stations = []
    for station in stations:
        if not MonitoringStation.typical_range_consistent(station):
            inconsistent_stations.append(station)
    return inconsistent_stations


class FlowMonitoringStation:
    """This class represents a flow monitoring station"""

    def __init__(self, measure_id, label, coord, typical_range, catchment,
                 river, town):
        self.measure_id = measure_id

        # Handle case of erroneous data where data system returns
        # '[label, label]' rather than 'label'
        self.name = label
        if isinstance(label, list):
            self.name = label[0]

        self.coord = coord
        self.typical_range = typical_range
        self.river = river
        self.catchment = catchment
        self.town = town
        self.latest_flow = None

    def __repr__(self):
        d = "Station name:         {}\n".format(self.name)
        d += "   measure id:        {}\n".format(self.measure_id)
        d += "   coordinate:        {}\n".format(self.coord)
        d += "   river:             {}\n".format(self.river)
        d += "   typical range:     {}".format(self.typical_range)
        d += "   catchment:         {}\n".format(self.catchment)
        return d

    def typical_range_consistent(self):
        """
        Checks the typical high/low range data for consistency.
        The method should return True if the data is consistent and False if the data is inconsistent or unavailable.
        Consistency is defined as when the typical high range is larger than the typical low range
        """
        if self.typical_range is None or len(self.typical_range) != 2:
            return False
        elif self.typical_range[0] > self.typical_range[1]:
            return False
        elif self.typical_range[0] is None or self.typical_range[1] is None:
            return False
        else:
            return True

    def relative_flow(self):
        """
        Returns the latest flow as a fraction of the typical range.
        i.e. a ratio of 1.0 corresponds to a flow at the typical high and
        a ratio of 0.0 corresponds to a flow at the typical low.

        """
        if self.typical_range_consistent() is True and self.latest_flow is not None:  # i.e. if the typical range is correctly presented
            return (self.latest_flow - self.typical_range[0]) / (self.typical_range[1] - self.typical_range[0])
        else:
            return None