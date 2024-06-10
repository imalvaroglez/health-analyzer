import folium


def plot_route(m, df, color="blue"):
    route = list(zip(df['latitude'], df['longitude']))
    folium.PolyLine(route, color=color, weight=2.5, opacity=1).add_to(m)


def create_map(center_location, zoom_start=13):
    return folium.Map(location=center_location, zoom_start=zoom_start)


def save_map(m, map_path):
    m.save(map_path)
