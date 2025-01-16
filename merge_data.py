import pandas as pd


def get_players_during_full_dzone(dzone_events, tracking_data):
    """
    Retrieves all players on the ice during the full defensive zone duration,
    including their location (X, Y), event type, and matching player details.

    Parameters:
    - dzone_events (DataFrame): Data of DZone events with 'Clock' and 'Period' columns.
    - tracking_data (DataFrame): Tracking data containing player information with 'Game Clock' and 'Period'.

    Returns:
    - DataFrame: A DataFrame with all players on the ice during the full defensive zone duration.
    """
    # Rename columns for consistency
    tracking_data = tracking_data.rename(columns={'Game Clock': 'Clock'})

    # Ensure 'Clock' is treated as strings for consistent merging
    tracking_data['Clock'] = tracking_data['Clock'].astype(str)
    dzone_events['Clock'] = dzone_events['Clock'].astype(str)

    result = []

    # Iterate through each period to capture full intervals
    for period in dzone_events['Period'].unique():
        # Filter events for the current period
        period_events = dzone_events[dzone_events['Period'] == period]

        # Determine the time range the puck was in the defensive zone
        min_time = period_events['Clock'].min()  # Earliest defensive zone entry
        max_time = period_events['Clock'].max()  # Latest defensive zone exit

        # Filter tracking data for this time interval
        period_tracking_data = tracking_data[
            (tracking_data['Period'] == period) &
            (tracking_data['Clock'] >= min_time) &
            (tracking_data['Clock'] <= max_time)
            ]

        # Merge with the defensive zone events to capture player details
        merged_data = pd.merge(
            period_events,
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
tracking_file_path = '/Users/alexlee/Desktop/DATATHON/2024-10-25.Team.H.@.Team.G.-.Tracking.csv'
dzone_events_file_path = '/Users/alexlee/Desktop/DATATHON/TeamH_DZone_Events.csv'

tracking_data = pd.read_csv(tracking_file_path)
dzone_events_data = pd.read_csv(dzone_events_file_path)

# Apply the function to get the full merged data
players_on_ice_during_dzone = get_players_during_full_dzone(dzone_events_data, tracking_data)

# Save the result to a CSV file
output_file_path = '/Users/alexlee/Desktop/DATATHON/players_on_ice_during_dzone123.csv'
players_on_ice_during_dzone.to_csv(output_file_path, index=False)

output_file_path