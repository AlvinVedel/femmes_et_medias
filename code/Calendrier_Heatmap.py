import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
import plotly.offline as py_offline

# Load your data
df23 = pd.read_csv("C:\\Users\\dinah\\Downloads\\data_gpi_2023.csv", sep="\t")
df23['date'] = pd.to_datetime(df23['date'])

# Extract additional date components
df23['month'] = df23['date'].dt.month
df23['day'] = df23['date'].dt.day
df23['day_of_week'] = df23['date'].dt.dayofweek  # Monday=0, Sunday=6
df23['week_of_month'] = df23['date'].apply(lambda d: (d.day-1) // 7 + 1)

# Define the colorscale before its first use
custom_colorscale = [
    [0, 'rgba(33, 113, 181, 0.85)'],  # Deep blue for the lowest values
    [0.5, 'rgba(255, 255, 255, 0.85)'], # Pure white for midpoint
    [1, 'rgba(233, 30, 99, 0.85)']  # Bright pink for the highest values
]

# Create subplots: 4 rows, 3 cols for the 12 months
fig = make_subplots(rows=4, cols=3, subplot_titles=[calendar.month_name[i] for i in range(1, 13)], shared_yaxes=True)

average_gpi = df23['gpi'].mean()

for month in range(1, 13):  # Include all months
    month_df = df23[df23['month'] == month]
    if not month_df.empty:
        heatmap = go.Heatmap(
            z=month_df['gpi'],
            x=month_df['day_of_week'],
            y=month_df['week_of_month'],
            colorscale=custom_colorscale,
            colorbar=dict(title='Femmes', tickvals=[]),  
            showscale=True,  
            xgap=3,
            ygap=3,
            zmid=average_gpi
        )
        row = (month - 1) // 3 + 1
        col = (month - 1) % 3 + 1
        fig.add_trace(heatmap, row=row, col=col)

# Update layout for better readability
fig.update_layout(
    height=1200,
    #title_text='GPI Calendar Heatmap for 2022',
    plot_bgcolor='white',
    paper_bgcolor='white'
)

fig.add_annotation(
    text="Hommes",  # Replace this with your desired text
    xref="paper",  # Use 'paper' for positioning relative to the entire figure
    yref="paper",
    x=1.075,  # Adjust this value to align with the right side of your figure
    y=-0.01,  # Adjust this value to position below the colorbar
    showarrow=False,
    font=dict(size=15)  # Adjust font size as needed
)

# Update xaxis and yaxis titles
axis_updates = {'tickmode': 'array', 'tickvals': list(range(7))}
for axis in fig.layout:
    if axis.startswith('x'):
        fig.layout[axis].update(**axis_updates, ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    elif axis.startswith('y'):
        # Adjusted to ensure correct update is applied to y-axes
        fig.layout[axis].update(**axis_updates, ticktext=[str(i) for i in range(1, 6)])

fig.show()
py_offline.plot(fig, filename='Calender.html')

# Assuming you are in a Jupyter notebook environment or similar that can render Plotly figures
# If you need to save the plot as an HTML file:
# py_offline.plot(fig, filename='Calendar.html')
