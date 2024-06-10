import gpxpy
import pandas as pd


def parse_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    data = [(point.latitude, point.longitude, point.elevation, point.time)
            for track in gpx.tracks for segment in track.segments for point in segment.points]
    return pd.DataFrame(data, columns=['latitude', 'longitude', 'elevation', 'time'])
