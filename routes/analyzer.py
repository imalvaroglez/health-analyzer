from geopy.distance import geodesic


def calculate_total_distance(df):
    total_distance = 0.0
    for i in range(1, len(df)):
        start = (df.iloc[i-1]['latitude'], df.iloc[i-1]['longitude'])
        end = (df.iloc[i]['latitude'], df.iloc[i]['longitude'])
        total_distance += geodesic(start, end).kilometers
    return total_distance


def calculate_elevation_gain(df):
    elevation_gain = 0.0
    for i in range(1, len(df)):
        gain = df.iloc[i]['elevation'] - df.iloc[i-1]['elevation']
        if gain > 0:
            elevation_gain += gain
    return elevation_gain
