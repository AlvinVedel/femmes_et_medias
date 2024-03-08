import plotly.graph_objs as go
import plotly.offline as py_offline
import pandas as pd
# Assuming 'tableau' has columns 'year', 'female_percentage', and 'female_editor_percentage'

merged_df = pd.read_csv(r"..\web\data\merged_df.csv", sep=",")
# Create traces
trace1 = go.Scatter(
    x=merged_df['year'],
    y=merged_df['female_percentage'],
    mode='lines+markers',
    name='Pourcentage de femmes Présentatrices',
    line=dict(color='brown')
)

trace2 = go.Scatter(
    x=merged_df['year'],
    y=merged_df['female_edit_percentage'],
    mode='lines+markers',
    name='Pourcentage de femmes Editrices',
    line=dict(color='orange')
)

# Combine traces
data = [trace1, trace2]

# Layout
layout = go.Layout(
    xaxis=dict(title='Années'),
    yaxis=dict(title='Pourcentage(%)'),
    showlegend=True
)

fig = go.Figure(data=data, layout=layout)

# Plot
py_offline.plot(fig, filename='../web/analyse/female_percentages_by_year.html')

