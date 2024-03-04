import pandas as pd
import plotly.express as px

csv_file_path = '/Users/angelacao/S2S/keypoints_data.csv'

df = pd.read_csv(csv_file_path)

# Filter rows where 'keypoint_type' is equal to 'face' and 'keypoint_number' is equal to 0
filtered_df = df[(df['keypoint_type'] == 'face') & (df['keypoint_number'] == 0)]

# Create a line graph using Plotly with separate lines for x, y, and z
fig = px.line(filtered_df, x='frame_number', y=['x', 'y', 'z'],
              title='x, y, z vs frame for face keypoint 0 (Upper-center Lip)',
              labels={'value': 'Keypoint Value', 'frame_number': 'Frame Number'})

# Show the plot
fig.show()
