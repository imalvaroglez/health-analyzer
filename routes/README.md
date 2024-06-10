# GPX Analyzer
This is a Python library for analyzing GPX files exported from Apple Health. It provides functions for parsing GPX files, calculating metrics such as total distance and elevation gain, and generating an interactive HTML map of all routes.

## Installation
To install the GPX Analyzer, you can use pip:


# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
pip install gpx-analyzer
## Usage
### Parsing GPX Files
You can parse GPX files using the parse_gpx function. This function takes a file path as input and returns a Pandas DataFrame containing information about each trackpoint in the GPX file.


# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import gpx_handler

gpx_file = "/path/to/my/gpx/file.gpx"
df = gpx_handler.parse_gpx(gpx_file)
### Calculating Metrics
The GPX Analyzer provides several functions for calculating metrics such as total distance and elevation gain. These functions can be used on the output of the parse_gpx function to calculate metrics for individual GPX files or for groups of GPX files.

For example, to calculate the total distance for a single GPX file:


# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import gpx_handler
import analyzer

gpx_file = "/path/to/my/gpx/file.gpx"
df = gpx_handler.parse_gpx(gpx_file)
total_distance = analyzer.calculate_total_distance(df)
To calculate the total distance and elevation gain for all GPX files in a directory:


# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import gpx_handler
import analyzer

gpx_folder = "/path/to/my/gpx/folder"
all_data = []

for filename in os.listdir(gpx_folder):
    if filename.endswith(".gpx"):
        filepath = os.path.join(gpx_folder, filename)
        df = gpx_handler.parse_gpx(filepath)
        df["filename"] = filename
        all_data.append(df)

workouts_df = pd.concat(all_data, ignore_index=True)
workouts_df["total_distance"] = workouts_df.groupby("filename").apply(
    lambda group: analyzer.calculate_total_distance(group.reset_index(drop=True))
).reset_index(drop=True)
workouts_df["elevation_gain"] = workouts_df.groupby("filename").apply(
    lambda group: analyzer.calculate_elevation_gain(group.reset_index(drop=True))
).reset_index(drop=True)
### Generating a Map
The GPX Analyzer provides a function for generating an interactive HTML map of all routes. The function create_map creates a folium map centered at a given location and adds markers for each trackpoint in a given Pandas DataFrame.


# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import gpx_handler
import maps

gpx_folder = "/path/to/my/gpx/folder"
all_data = []

for filename in os.listdir(gpx_folder):
    if filename.endswith(".gpx"):
        filepath = os.path.join(gpx_folder, filename)
        df = gpx_handler.parse_gpx(filepath)
        df["filename"] = filename
        all_data.append(df)

workouts_df = pd.concat(all_data, ignore_index=True)

if not workouts_df.empty:
    center_location = [
        workouts_df["latitude"].mean(), workouts_df["longitude"].mean()
    ]
    m = maps.create_map(center_location)

    for filename in workouts_df["filename"].unique():
        route_df = workouts_df[workouts_df["filename"] == filename]
        maps.plot_route(m, route_df)

    map_path = "all_routes.html"
    maps.save_map(m, map_path)