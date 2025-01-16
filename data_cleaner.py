import pandas as pd

def filter_defensive_zone(data, x_min=-100, x_max=-25):
    """
    Filters events to include those where the puck enters the defensive zone.
    The defensive zone is defined by x-coordinates within [x_min, x_max].
    Includes the event just before entering and after exiting the defensive zone.
    """
    filtered_rows = []
    in_zone = False

    for i, row in data.iterrows():
        x_coord = row['X_Coordinate']

        # Check if in defensive zone
        if x_min <= x_coord <= x_max:
            if not in_zone:
                # Add the event just before entering the zone
                if i > 0:
                    filtered_rows.append(data.iloc[i - 1])
            in_zone = True
            filtered_rows.append(row)
        else:
            if in_zone:
                # Add the event just after exiting the zone
                filtered_rows.append(row)
            in_zone = False

    # Create a new DataFrame from the filtered rows
    filtered_df = pd.DataFrame(filtered_rows)
    return filtered_df

# Load the uploaded CSV file
file_path = '/Users/alexlee/Desktop/DATATHON/2024-10-25.Team.H.@.Team.G.-.Events.csv'
# Replace with your file path
data = pd.read_csv(file_path)

# Apply the function to filter the data
filtered_data = filter_defensive_zone(data)

# Save the filtered data to a new CSV
output_file_path = '/Users/alexlee/Desktop/DATATHON/TeamH_DZone_Events.csv'  # Replace with your desired output path
filtered_data.to_csv(output_file_path, index=False)

print(f"Filtered data saved to ")


