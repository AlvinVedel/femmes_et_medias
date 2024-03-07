import pandas as pd
from ast import literal_eval
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly.offline as py_offline
import plotly.io as pio
from IPython.display import display, HTML



df = pd.read_csv(r"..\data\data_cluster_gpi\df_total.csv", sep='\t')
df = df.loc[df['media'].isin(['TF1', 'France 2', 'France 3'])]

unique_mots_clefs = df['mots_clefs'].unique()
# Simulation d'une liste similaire à df['mots_clefs'].unique()
# avec des chaînes représentant des listes de tuples (mot, probabilité)
unique_mots_clefs = df['mots_clefs'].unique()

# Utilisation de literal_eval pour convertir les chaînes en listes de tuples, puis extraction des mots
list_of_lists_of_words_fixed = [[word_tuple[0] for word_tuple in literal_eval(mots_clefs_string)] for mots_clefs_string in unique_mots_clefs]

# Création d'une nouvelle colonne 'liste_mots_clefs' qui contient les listes des mots-clés
df['liste_mots_clefs'] = df['mots_clefs'].apply(lambda x: [word_tuple[0] for word_tuple in literal_eval(x)])

# Modification de la création de la colonne 'liste_mots_clefs' pour conserver uniquement le top 5 des mots-clés par probabilité
df['liste_mots_clefs_top5'] = df['mots_clefs'].apply(
    lambda x: [word_tuple[0] for word_tuple in sorted(literal_eval(x), key=lambda item: item[1], reverse=True)[:7]]
)

# Transformation de la colonne 'liste_mots_clefs' en une chaîne unique pour chaque liste
df['liste_de_mot_str'] = df['liste_mots_clefs_top5'].apply(lambda x: ','.join(x))

# Groupement par la nouvelle colonne chaîne de caractères et par média, puis calcul de la moyenne de 'gpi'
gpi_moyen_par_combinaison = df.groupby(["liste_de_mot_str", "media"]).gpi.mean().reset_index()


# Correction appliquée ici
heatmap_data = gpi_moyen_par_combinaison.pivot(index="liste_de_mot_str", columns="media", values="gpi")

# Exemple de données pour l'illustration
min_val, max_val = -1, 1  # Exemple de valeurs min et max pour votre GPI
zero_norm = abs(0 - min_val) / (max_val - min_val)  # Normalisation de la position de zéro

# Définition de l'échelle de couleurs personnalisée avec des nuances plus prononcées
custom_colorscale = [
    [0, 'rgba(33, 113, 181, 0.85)'],    # Bleu profond pour les valeurs les plus basses
    [zero_norm, 'rgba(255, 255, 255, 0.85)'],  # Blanc pur pour zéro
    [1, 'rgba(233, 30, 99, 0.85)']      # Rose vif pour les valeurs les plus hautes
]

# Préparation du texte de survol
hovertext = []
for i in range(len(heatmap_data.index)):
    hovertext.append([])
    for j in range(len(heatmap_data.columns)):
        hovertext[i].append('GPI: {}<br>Cluster: {}<br>Media: {}'.format(
            heatmap_data.values[i, j],  # Valeur GPI
            heatmap_data.index[i],      # Cluster (ou toute autre info de ligne)
            heatmap_data.columns[j]     # Média (ou toute autre info de colonne)
        ))

#Création de la heatmap avec Plotly, maintenant avec des gaps et une échelle de couleurs personnalisée
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale=custom_colorscale,
    hoverinfo="text",
    text=hovertext,
    hoverongaps=False,
    xgap=3,  # Ajout d'un petit espace entre les colonnes pour séparer les carrés
    ygap=3,   # Ajout d'un petit espace entre les rangées pour séparer les carrés
    zmid=-0.5
))

# Configuration de la figure avec des dimensions ajustées pour favoriser des cellules plus carrées
fig_width = 900  # Ajustez selon votre besoin
num_x_categories = len(heatmap_data.columns)
num_y_categories = len(heatmap_data.index) 
square_size = 30  # Ajustez selon votre besoin pour la taille des carrés

fig.update_layout(
    xaxis_title='Média',
    yaxis_title='Mots-clés',
    xaxis=dict(tickangle=-45, showgrid=False),  # Enlever la grille pour l'axe X et incliner les étiquettes
    yaxis=dict(showgrid=False),  # Enlever la grille pour l'axe Y
    autosize=False,
    width=fig_width,
    height=square_size * num_y_categories,  # Ajuster la hauteur pour permettre des cellules plus carrées
    margin=dict(l=50, r=50, t=50, b=50),  # Ajustez les marges selon le besoin
    plot_bgcolor='rgba(255,255,255,1)',  # Définir le fond du graphique en blanc
    paper_bgcolor='rgba(255,255,255,1)'  # Définir le fond de la figure en blanc
)

# Affichage de la figure
fig.show()

# 'fig' devrait être votre objet figure Plotly
plot_html = py_offline.plot(fig, filename='../web/heat_map_plot.html', auto_open=False)
