from dash import html, dcc

def create_layout(app):
    return html.Div(
        children=[
            html.H1("NFT Market Dashboard", style={"textAlign": "center"}),

            # Scatter plot graph
            dcc.Graph(id="scatter_plot"),

            # Dropdown for selecting NFT clusters
            html.Div(
                children=[
                    dcc.Dropdown(
                        id="cluster_dropdown",
                        options=[{"label": f"Cluster {i}", "value": i} for i in range(3)],
                        value=0,
                        clearable=False,
                        style={"width": "50%", "margin": "auto"},
                    )
                ],
                style={"textAlign": "center", "marginBottom": "20px"},
            ),

            # Clustering visualization graph
            dcc.Graph(id="cluster_plot"),
        ]
    )
