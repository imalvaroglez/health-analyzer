import gpx_handler
import analyzer
import maps

import os
import pandas as pd
from tqdm import tqdm

gpx_folder = "/Users/imalvaroglez/Downloads/apple_health_export/workout-routes"
all_data = []

# Create progress bar for reading files
files = [f for f in os.listdir(gpx_folder) if f.endswith('.gpx')]
with tqdm(total=len(files), desc="Processing GPX files") as pbar:
    for filename in files:
        filepath = os.path.join(gpx_folder, filename)
        df = gpx_handler.parse_gpx(filepath)
        df['filename'] = filename
        all_data.append(df)
        pbar.update(1)

workouts_df = pd.concat(all_data, ignore_index=True)

workouts_df['total_distance'] = workouts_df.groupby('filename').apply(
    lambda group: analyzer.calculate_total_distance(
        group.reset_index(drop=True))
).reset_index(drop=True)

workouts_df['elevation_gain'] = workouts_df.groupby('filename').apply(
    lambda group: analyzer.calculate_elevation_gain(
        group.reset_index(drop=True))
).reset_index(drop=True)

# Calculate statistics
stats = {
    'Total Workouts': len(workouts_df['filename'].unique()),
    'Total Distance (km)': workouts_df['total_distance'].sum(),
    'Total Elevation Gain (m)': workouts_df['elevation_gain'].sum(),
    'Average Distance (km)': workouts_df['total_distance'].mean(),
    'Average Elevation Gain (m)': workouts_df['elevation_gain'].mean(),
}

# Print statistics
print("\nStatistics:")
for stat, value in stats.items():
    print(f"- {stat}: {value}")

# Create a single map for all routes
if not workouts_df.empty:
    center_location = [
        workouts_df['latitude'].mean(), workouts_df['longitude'].mean()]
    m = maps.create_map(center_location)

    # Create progress bar for plotting routes
    unique_files = workouts_df['filename'].unique()
    with tqdm(total=len(unique_files), desc="Adding routes to map") as pbar:
        for filename in unique_files:
            route_df = workouts_df[workouts_df['filename'] == filename]
            maps.plot_route(m, route_df)
            pbar.update(1)

    map_path = "all_routes.html"
    maps.save_map(m, map_path)
