import plotly.graph_objs as go
import plotly.offline as py_offline
import pandas as pd
# Assuming 'tableau' has columns 'year', 'female_percentage', and 'female_editor_percentage'

merged_df = pd.read_csv("C:\\Users\\dinah\\Downloads\\merged_df.csv", sep=",")

# Create traces
trace1 = go.Scatter(
    x=merged_df['year'],
    y=merged_df['female_percentage'],
    mode='lines+markers',
    name='Female Presenter Percentage',
    line=dict(color='brown')
)

trace2 = go.Scatter(
    x=merged_df['year'],
    y=merged_df['female_edit_percentage'],
    mode='lines+markers',
    name='Female Editor Percentage',
    line=dict(color='orange')
)

# Combine traces
data = [trace1, trace2]

# Layout
layout = go.Layout(
    title='Percentage of Female Editors and Presentaters by Year',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Percentage'),
    showlegend=True
)

fig = go.Figure(data=data, layout=layout)

# Plot
py_offline.plot(fig, filename='female_percentages_by_year.html')

