import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
import pandas as pd
from ast import literal_eval
import plotly.express as px
import plotly.offline as py_offline
import plotly.io as pio


df = pd.read_csv(r"..\data\data_cluster_gpi\df_total.csv", sep='\t')

# Préparation des données pour l'histogramme et la courbe de densité
density = gaussian_kde(df['gpi'])
xs = np.linspace(df['gpi'].min(), df['gpi'].max(), 200)
total_articles = len(df['gpi'])
bin_width = (df['gpi'].max() - df['gpi'].min()) / 40  # Nombre de bins
ys = density(xs) * total_articles * bin_width

# Création de l'histogramme avec un texte de survol personnalisé
histogram = go.Histogram(
    x=df['gpi'], 
    nbinsx=40, 
    name='Histogramme', 
    marker_color='#322c2d',
    hoverinfo='y',
    hovertemplate='<b>Intervalle du GPI:</b> %{x}<br><b>Nombre d\'articles:</b> %{y}<extra></extra>'
)

# Ajout de la courbe de densité ajustée avec son propre texte de survol
density_trace = go.Scatter(
    x=xs, 
    y=ys, 
    mode='lines', 
    name='Densité', 
    line=dict(color='#f26522'),
    hoverinfo='x+y',
    hovertemplate='<b>Valeur du GPI:</b> %{x:.2f}<br><b>Densité estimée:</b> %{y:.2f}<extra></extra>'
)

# Construction de la figure avec les deux traces
fig = go.Figure(data=[histogram, density_trace])

# Mise à jour des paramètres de la mise en page
fig.update_layout(
    xaxis_title='Indice de Parité de Genre Ajusté (GPI)',
    yaxis_title='Nombre d\'Articles',
    bargap=0.05,  # Espace entre les barres
    template='plotly_white'
)

# Affichage de la figure
fig.show()

# 'fig' devrait être votre objet figure Plotly
py_offline.plot(fig, filename='../web/gpi_distrib.html', auto_open=False)
