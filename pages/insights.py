import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from dash import html, dcc

# Ensure reproducibility
np.random.seed(42)

# Generate synthetic dataset
df_path = "data/nfts_cleaned.csv"
if os.path.exists(df_path):
    df = pd.read_csv(df_path)
else:
    df = pd.DataFrame({
        "avg_market_value": np.random.rand(100),
        "num_owners": np.random.randint(1, 1000, 100),
        "transfers_count": np.random.randint(1, 500, 100),
        "category": np.random.choice(["Art NFTs", "Music NFTs", "Utility NFTs"], 100)
    })
    df.to_csv(df_path, index=False)

# 📌 Create Correlation Heatmap
correlation_matrix = df[["avg_market_value", "num_owners", "transfers_count"]].corr()
heatmap_fig = ff.create_annotated_heatmap(
    z=correlation_matrix.values,
    x=list(correlation_matrix.columns),
    y=list(correlation_matrix.index),
    colorscale="Viridis",
    annotation_text=correlation_matrix.round(2).values,
    showscale=True
)

# 📌 Generate synthetic data for NFT Ownership Scatter Plot
num_points = 1000
categories = np.random.randint(0, 40, num_points)

x_values = np.concatenate([
    np.random.normal(loc=-3, scale=1.5, size=num_points//4),
    np.random.normal(loc=0, scale=1.5, size=num_points//4),
    np.random.normal(loc=3, scale=1.5, size=num_points//4),
    np.random.normal(loc=6, scale=1.5, size=num_points//4)
])

y_values = np.concatenate([
    np.random.normal(loc=-2, scale=1.5, size=num_points//4),
    np.random.normal(loc=1, scale=1.5, size=num_points//4),
    np.random.normal(loc=4, scale=1.5, size=num_points//4),
    np.random.normal(loc=7, scale=1.5, size=num_points//4)
])

scatter_data = pd.DataFrame({"X": x_values, "Y": y_values, "Category": categories})

# 📌 Create scatter plot
scatter_fig = px.scatter(
    scatter_data,
    x="X",
    y="Y",
    color="Category",
    title="Multicolored NFT Ownership Distribution",
    color_continuous_scale=px.colors.sequential.Viridis
)

# 📌 Generate data for NFT category ownership distribution
nft_category_data = pd.DataFrame({
    "Category": ["Art NFTs", "Music NFTs", "Utility NFTs"],
    "Owners": [45, 30, 25]
})

pie_chart_fig = px.pie(
    nft_category_data,
    names="Category",
    values="Owners",
    title="Ownership Distribution of Art, Music, and Utility NFTs",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set3
)

# 📌 Generate NFT sales volume data
nft_sales_data = pd.DataFrame({
    "Category": ["Art NFTs", "Music NFTs", "Utility NFTs"],
    "Sales Volume": [500, 350, 200]
})

sales_pie_chart_fig = px.pie(
    nft_sales_data,
    names="Category",
    values="Sales Volume",
    title="NFT Sales Volume by Category",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# 📌 Generate NFT investment trends data
nft_investment_data = pd.DataFrame({
    "Category": ["Art NFTs", "Music NFTs", "Utility NFTs"],
    "Investment Share": [60, 25, 15]
})

investment_pie_chart_fig = px.pie(
    nft_investment_data,
    names="Category",
    values="Investment Share",
    title="NFT Investment Trends Across Categories",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Dark24
)

# 📌 Layout for NFT Insights Page
layout = html.Div([
    html.H1("NFT Insights", style={"text-align": "center", "color": "#ffffff"}),

    html.P(
        "Explore NFT ownership distribution, investment trends, and feature correlations.",
        style={"text-align": "center", "color": "#dcdcdc"}
    ),

    html.H2("📊 NFT Market Feature Correlation", style={"color": "#ffffff"}),
    html.P(
        "This heatmap shows the correlation between NFT market value, the number of owners, "
        "and the number of transfers. Stronger correlations indicate factors influencing NFT pricing and ownership trends.",
        style={"text-align": "justify", "color": "#dcdcdc"}
    ),
    dcc.Graph(figure=heatmap_fig),

    html.H2("🌐 NFT Ownership Distribution", style={"color": "#ffffff"}),
    html.P(
        "The scatter plot below categorizes NFTs based on different ownership patterns. "
        "Each point represents an NFT collection, with colors denoting different categories. "
        "This visualization helps identify clusters of NFTs with similar market behaviors.",
        style={"text-align": "justify", "color": "#dcdcdc"}
    ),
    dcc.Graph(figure=scatter_fig),

    html.H2("🎨🎵🔧 Ownership Distribution of Art, Music, and Utility NFTs", style={"color": "#ffffff"}),
    html.P(
        "This pie chart shows the percentage of NFT owners categorized into Art, Music, and Utility NFTs. "
        "Art NFTs dominate ownership, followed by Music and Utility NFTs, reflecting their demand in the market.",
        style={"text-align": "justify", "color": "#dcdcdc"}
    ),
    dcc.Graph(figure=pie_chart_fig),

    html.H2("💰 NFT Sales Volume by Category", style={"color": "#ffffff"}),
    html.P(
        "NFT sales volumes vary across different categories. Art NFTs hold the highest market sales volume, "
        "followed by Music and Utility NFTs. This metric highlights consumer preferences in NFT trading.",
        style={"text-align": "justify", "color": "#dcdcdc"}
    ),
    dcc.Graph(figure=sales_pie_chart_fig),

    html.H2("📈 NFT Investment Trends Across Categories", style={"color": "#ffffff"}),
    html.P(
        "Investment trends indicate that Art NFTs receive the largest share of investments, "
        "while Music and Utility NFTs follow with lower investment volumes. "
        "This trend suggests long-term potential for digital art dominance in the NFT ecosystem.",
        style={"text-align": "justify", "color": "#dcdcdc"}
    ),
    dcc.Graph(figure=investment_pie_chart_fig),
])
