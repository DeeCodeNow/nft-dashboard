from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pages.home as home
import pages.insights as insights
import pages.trends as trends
import pages.comparison as comparison
import pages.data_insights as data_insights
import pages.nft_collections as nft_collections

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "NFT Market Dashboard"

# Layout with Sidebar for Navigation
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("NFT Dashboard", className="sidebar-title"),
            dbc.Nav([
                dbc.NavLink("🏠 Home", href="/", active="exact"),
                dbc.NavLink("📊 Insights", href="/insights", active="exact"),
                dbc.NavLink("📈 Trends", href="/trends", active="exact"),
                dbc.NavLink("🔄 Compare", href="/comparison", active="exact"),
                dbc.NavLink("📊 Market Insights", href="/data_insights", active="exact"),
                dbc.NavLink("📂 NFT Collections", href="/nft_collections", active="exact"),
            ], vertical=True, pills=True, className="sidebar-nav"),
        ], width=2, className="sidebar"),
        
        dbc.Col([
            dcc.Location(id="url"),
            html.Div(id="page-content")
        ], width=10),
    ])
], fluid=True)

# Callback to control page navigation
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/insights":
        return insights.layout
    elif pathname == "/trends":
        return trends.layout
    elif pathname == "/comparison":
        return comparison.layout
    elif pathname == "/data_insights":
        return data_insights.layout
    elif pathname == "/nft_collections":
        return nft_collections.layout
    else:
        return home.layout

# 📌 Register Callbacks
comparison.register_callbacks(app)  # Ensure comparison page callbacks work
nft_collections.register_callbacks(app)  # Ensure NFT Collections page callbacks work
trends.register_callbacks(app)  # Register the callback for graph updates

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

