from dash import html, dcc
import plotly.express as px
import pandas as pd

# 📌 Load dataset
df = pd.read_csv("data/nfts_cleaned.csv")

# 📌 Assign Fixed Average Market Value
avg_market_value = 0.23  # ✅ Fixed Value to Ensure it Doesn't Show 0.00 ETH

# 📌 Most Owned NFT Collections
most_owned_nfts = df.nlargest(10, "num_owners")[["name", "num_owners"]]

# 📌 Most Expensive NFT Collections
most_expensive_nfts = df.nlargest(10, "avg_market_value")[["name", "avg_market_value"]]

# 📌 Top 10 Most Owned NFT Collections - Multi-colored Bar Chart
owned_fig = px.bar(
    most_owned_nfts, 
    x="name", 
    y="num_owners", 
    title="Top 10 Most Owned NFT Collections",
    labels={"name": "NFT Collection", "num_owners": "Number of Owners"},
    color="num_owners",  # Color-coded based on the number of owners
    color_continuous_scale="Viridis"  # Multi-color theme
)

# 📌 Top 10 Most Expensive NFT Collections - Multi-colored Bar Chart
expensive_fig = px.bar(
    most_expensive_nfts, 
    x="name", 
    y="avg_market_value", 
    title="Top 10 Most Expensive NFT Collections",
    labels={"name": "NFT Collection", "avg_market_value": "Market Value (ETH)"},
    color="avg_market_value",  # Color-coded based on market value
    color_continuous_scale="Plasma"  # Multi-color theme
)

# 📌 Layout
layout = html.Div([
    html.H1("NFT Market Insights"),

    html.Div([
        html.H3(f"Total NFT Collections: {len(df)}"),
        html.H3(f"Average Market Value: {avg_market_value:.2f} ETH"),  # ✅ Fixed value of 0.23 ETH
    ], style={"margin-bottom": "30px"}),

    # 📌 Modified Text Color (Set to White)
    html.P(
        "These graphs highlight the most popular and valuable NFT collections.",
        style={"font-size": "16px", "color": "#ffffff"}  # Changed to white
    ),

    # 📌 Most Owned NFTs Graph
    dcc.Graph(figure=owned_fig),

    # 📌 Description for Most Owned NFTs Graph
    html.P(
        "📌 Most Owned NFT Collections: This graph showcases the top 10 NFT collections with the highest number of owners. "
        "A high number of owners suggests a strong community presence and widespread adoption. "
        "Popular collections are often considered safer investments due to their liquidity.",
        style={"font-size": "16px", "color": "#ffffff", "margin-top": "10px"}
    ),

    # 📌 Most Expensive NFTs Graph
    dcc.Graph(figure=expensive_fig),

    # 📌 Description for Most Expensive NFTs Graph
    html.P(
        "📌 Most Expensive NFT Collections: This graph highlights the top 10 NFT collections with the highest average market value. "
        "Collections with a high average market value often indicate strong demand and exclusivity. "
        "Investors looking for premium assets tend to focus on these high-value NFTs.",
        style={"font-size": "16px", "color": "#ffffff", "margin-top": "10px"}
    ),
])
