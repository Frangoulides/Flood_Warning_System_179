def plot_water_levels(station, dates, levels):
    import matplotlib.pyplot as plt

    plt.plot(dates, levels)

    plt.xlabel('date')
    plt.ylabel('water level (m)')
    plt.xticks(rotation=45)
    plt.title(station.name)
    plt.axhline(y=station.typical_range[0], markersize=10, linestyle='dashed')
    plt.axhline(y=station.typical_range[1], markersize=8, linestyle='dashed')

    plt.tight_layout()

    plt.show()
