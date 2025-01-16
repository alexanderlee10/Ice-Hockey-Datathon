import pandas as pd
from datetime import datetime, timedelta

def generate_time_intervals(start_time, end_time):
    """
    Generates a list of time strings between start_time and end_time at one-second intervals.
    """
    time_format = "%M:%S"
    start = datetime.strptime(start_time, time_format)
    end = datetime.strptime(end_time, time_format)
    time_intervals = []
    while start >= end:
        time_intervals.append(start.strftime(time_format))
        start -= timedelta(seconds=1)
    return time_intervals

def get_players_during_full_dzone_with_intervals(dzone_events, tracking_data):
    """
    Retrieves all players on the ice during the full defensive zone duration,
    including every second within the intervals.

    Parameters:
    - dzone_events (DataFrame): Data of DZone events with 'Clock' and 'Period' columns.
    - tracking_data (DataFrame): Tracking data containing player information with 'Game Clock' and 'Period'.

    Returns:
    - DataFrame: A DataFrame with all players on the ice during the full defensive zone duration.
    """
    # Ensure the required columns exist
    if 'Clock' not in dzone_events.columns:
        raise KeyError("The 'Clock' column is missing in dzone_events. Check your data or column names.")
    if 'Clock' not in tracking_data.columns:
        tracking_data = tracking_data.rename(columns={'Game Clock': 'Clock'})

    # Ensure 'Clock' is treated as strings for consistent merging
    tracking_data['Clock'] = tracking_data['Clock'].astype(str)
    dzone_events['Clock'] = dzone_events['Clock'].astype(str)

    result = []

    # Iterate through each period to capture full intervals
    for period in dzone_events['Period'].unique():
        # Filter events for the current period
        period_events = dzone_events[dzone_events['Period'] == period]

        # Group by intervals
        for _, group in period_events.groupby('Period'):
            min_time = group['Clock'].min()  # Earliest defensive zone entry
            max_time = group['Clock'].max()  # Latest defensive zone exit

            # Generate all time intervals within the range
            time_intervals = generate_time_intervals(max_time, min_time)

            # Filter tracking data for this time interval
            period_tracking_data = tracking_data[
                (tracking_data['Period'] == period) &
                (tracking_data['Clock'].isin(time_intervals))
            ]

            # Merge with the defensive zone events to capture player details
            merged_data = pd.merge(
                group,
                period_tracking_data,
                on=['Period', 'Clock'],
                how='inner'
            )

            # Append the merged data
            result.append(merged_data)

    # Combine all intervals into a single DataFrame
    result_df = pd.concat(result, ignore_index=True)

    # Handle the Team columns (`Team_x` or `Team_y`)
    if 'Team_x' in result_df.columns:
        result_df['Team'] = result_df['Team_x']
    elif 'Team_y' in result_df.columns:
        result_df['Team'] = result_df['Team_y']

    # Include only relevant columns for output
    result_df = result_df[['Period', 'Clock', 'Player Id', 'Team', 'Player or Puck',
                           'Rink Location X (Feet)', 'Rink Location Y (Feet)',
                           'X_Coordinate', 'Y_Coordinate', 'Event']]

    return result_df

# Load the data from the provided CSV files
dzone_events_file_path = '/Users/alexlee/Desktop/DATATHON/TeamH_DZone_Events.csv'
tracking_file_path = '/Users/alexlee/Desktop/DATATHON/2024-10-25.Team.H.@.Team.G.-.Tracking.csv'

dzone_events_data = pd.read_csv(dzone_events_file_path)
tracking_data = pd.read_csv(tracking_file_path)

# Verify the column names
print("dzone_events_data columns:", dzone_events_data.columns)
print("tracking_data columns:", tracking_data.columns)

# Apply the function to get the full merged data with intervals
players_on_ice_during_dzone_intervals = get_players_during_full_dzone_with_intervals(dzone_events_data, tracking_data)

# Save the result to a CSV file
output_file_path = '/Users/alexlee/Desktop/DATATHON/testing15.csv'
players_on_ice_during_dzone_intervals.to_csv(output_file_path, index=False)

print(f"Data saved to {output_file_path}")

