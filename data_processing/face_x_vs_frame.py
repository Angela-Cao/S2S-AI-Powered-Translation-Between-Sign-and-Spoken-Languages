import pandas as pd
import plotly.express as px
csv_file_path = '/Users/angelacao/S2S/keypoints_data.csv'

df = pd.read_csv(csv_file_path)


#print(df.head())

# Filter rows where 'keypoint_type' is equal to 'face'
filtered_df = df[df['keypoint_type'] == 'face']

# Create a line graph using Plotly
fig = px.line(filtered_df, x='frame_number', y='x', color='keypoint_number', title='x vs frame')
fig.update_layout(xaxis_title='Frame Number', yaxis_title='Value of "x"')

# Show the plot
fig.show()
