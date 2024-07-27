# custom_theme.py

import plotly.graph_objs as go
import plotly.express as px

def create_custom_theme():
    custom_theme = go.layout.Template()

    # Set the font to monospace and minimum size to 14
    custom_theme.layout.font = dict(family="monospace", size=14)

    # Set the color scheme (dark theme with Viridis color scale)
    custom_theme.layout.plot_bgcolor = "#1e1e1e"
    custom_theme.layout.paper_bgcolor = "#1e1e1e"
    custom_theme.layout.colorway = px.colors.sequential.Viridis

    # Set text colors
    custom_theme.layout.font.color = "#ffffff"
    custom_theme.layout.title.font.color = "#ffffff"
    custom_theme.layout.xaxis.color = "#ffffff"
    custom_theme.layout.yaxis.color = "#ffffff"

    # Set grid colors
    custom_theme.layout.xaxis.gridcolor = "#333333"
    custom_theme.layout.yaxis.gridcolor = "#333333"

    return custom_theme

# Create an instance of the custom theme
custom_theme = create_custom_theme()