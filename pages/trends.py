from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Load dataset
df_path = "data/nfts_cleaned.csv"
try:
    df = pd.read_csv(df_path)
except FileNotFoundError:
    raise FileNotFoundError(f"⚠️ Dataset not found at {df_path}. Please check the file path.")

# 📌 Function to Get Top NFTs by Selected Metric
def get_top_nfts(metric, top_n=20):
    return df.nlargest(top_n, metric)[["name", metric]]

# 📌 Default Chart - Top 20 by Market Value
top_nfts = get_top_nfts("avg_market_value")
trend_fig = px.bar(
    top_nfts, 
    x="name", 
    y="avg_market_value", 
    title="Top 20 NFT Collections by Market Value",
    labels={"name": "NFT Collection", "avg_market_value": "Market Value (ETH)"},
    color="avg_market_value",
    height=550
)
trend_fig.update_xaxes(tickangle=30, tickmode="array", tickvals=list(range(len(top_nfts["name"]))))

# 📌 Layout
layout = html.Div([
    html.H1("Market Trends", style={"color": "#ffffff"}),

    html.P(
        "This chart displays the top 20 NFT collections based on different metrics. "
        "Use the dropdown below to explore rankings based on market value, number of owners, or transfer count.",
        style={"font-size": "16px", "color": "#dcdcdc"}
    ),

    # 📌 Interactive Dropdown for Metric Selection
    html.Label("Select Metric:", style={"font-weight": "bold", "color": "#ffffff"}),
    dcc.Dropdown(
    id="metric_dropdown",
    options=[
        {"label": "Market Value", "value": "avg_market_value"},
        {"label": "Number of Owners", "value": "num_owners"},
        {"label": "Number of Transfers", "value": "transfers_count"},
    ],
    value="avg_market_value",
    clearable=False,
    className="custom-dropdown",  # ✅ This matches our CSS fix
    style={
        "width": "250px",
        "color": "black",  # ✅ Ensure text remains visible
        "border-radius": "5px",
        "border": "none",
        "box-shadow": "none"
    }
),
    # 📌 Updated Graph
    dcc.Graph(id="trend_graph", figure=trend_fig),

    # 📌 Dynamic Description
    html.Div(id="trend_description", style={"font-size": "16px", "color": "#dcdcdc", "margin-top": "10px", "text-align": "justify"}),
])

# 📌 Callback for Updating Chart & Description
def register_callbacks(app):
    @app.callback(
        [Output("trend_graph", "figure"), Output("trend_description", "children")],
        Input("metric_dropdown", "value")
    )
    def update_trend_chart(selected_metric):
        if selected_metric not in df.columns:
            return trend_fig, "⚠️ Invalid metric selected!"

        updated_data = get_top_nfts(selected_metric)

        # 📌 Generate Graph
        fig = px.bar(
            updated_data, 
            x="name", 
            y=selected_metric, 
            title=f"Top 20 NFT Collections by {selected_metric.replace('_', ' ').title()}",
            labels={"name": "NFT Collection", selected_metric: selected_metric.replace('_', ' ').title()},
            color=selected_metric,
            height=550
        )
        fig.update_xaxes(tickangle=30, tickmode="array", tickvals=list(range(len(updated_data["name"]))))
        
        # 📌 Generate Dynamic Description
        if selected_metric == "avg_market_value":
            description = (
                "This chart showcases the top 20 NFT collections ranked by their average market value. "
                "Collections like Bored Ape Yacht Club and CryptoPunks continue to dominate the market, "
                "while emerging NFT projects are also gaining traction."
            )
        elif selected_metric == "num_owners":
            description = (
                "This graph highlights the NFT collections with the highest number of unique owners. "
                "A larger number of owners often indicates strong community engagement and widespread adoption."
            )
        elif selected_metric == "transfers_count":
            description = (
                "This chart ranks the top NFT collections based on the number of transfers. "
                "Higher transfer counts suggest increased liquidity and frequent trading activity, "
                "which can be a key indicator of market demand."
            )

        return fig, description
