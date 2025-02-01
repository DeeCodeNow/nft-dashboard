from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# 📌 Load dataset
df = pd.read_csv("data/nfts_cleaned.csv")

# 📌 Ensure 'sales_date' is properly parsed
df["sales_date"] = pd.to_datetime(df["sales_date"], errors="coerce")
df.dropna(subset=["sales_date"], inplace=True)

# 📌 Ensure 'collection_age' exists and is positive
df["collection_age"] = (pd.to_datetime("today") - df["sales_date"]).dt.days
df["collection_age"] = df["collection_age"].clip(lower=0)

# 📌 Ensure 'floor_price' exists
if "floor_price" not in df.columns:
    df["floor_price"] = df["avg_market_value"] * 0.8

# 📌 Save cleaned dataset
df.to_csv("data/nfts_cleaned.csv", index=False)

# 📌 Set Proper Filter Ranges
market_value_min, market_value_max = df["avg_market_value"].min(), df["avg_market_value"].max()
floor_price_min, floor_price_max = df["floor_price"].min(), df["floor_price"].max()
owners_min, owners_max = df["num_owners"].min(), df["num_owners"].max()
sales_min, sales_max = df["transfers_count"].min(), df["transfers_count"].max()
age_min, age_max = df["collection_age"].min(), df["collection_age"].max()

# 📌 Categorize NFTs
def categorize_nft(name):
    if any(keyword in name.lower() for keyword in ["ape", "punk", "azuki", "mutant"]):
        return "High-Value"
    elif any(keyword in name.lower() for keyword in ["sandbox", "axie", "decentraland"]):
        return "Gaming"
    elif any(keyword in name.lower() for keyword in ["pak", "fidenza", "art", "xc"]):
        return "Digital Art"
    elif any(keyword in name.lower() for keyword in ["ens", "proof", "moonbirds"]):
        return "Utility"
    else:
        return "Others"

df["category"] = df["name"].apply(categorize_nft)

# 📌 Category Descriptions
category_descriptions = {
    "High-Value": "🔹 High-Value NFTs include premium collections like Bored Ape Yacht Club, CryptoPunks, and Azuki. These NFTs have a strong market presence and often hold their value well in fluctuating markets.",
    "Gaming": "🎮 Gaming NFTs include digital assets used in blockchain games such as Axie Infinity, The Sandbox, and Decentraland. These NFTs represent in-game characters, weapons, or virtual land.",
    "Digital Art": "🎨 Digital Art NFTs are created by renowned artists like Pak, Beeple, and XCOPY. These NFTs represent exclusive digital artwork, animations, and generative art pieces.",
    "Utility": "🔑 Utility NFTs provide real-world or digital benefits beyond collectibles. Examples include ENS domain names, membership NFTs, and access tokens to exclusive communities.",
    "Others": "🌐 This category includes experimental NFTs, niche collections, and emerging projects that may include AI-generated content, music NFTs, or cross-chain assets."
}

# 📌 Filters Layout
filters_layout = html.Div([
    html.Label("🔹 Select NFT Category:", style={"font-weight": "bold"}),
    dcc.Dropdown(id="nft_category_dropdown",
                 options=[{"label": cat, "value": cat} for cat in df["category"].unique()],
                 value="High-Value",
                 clearable=False,
                 style={"width": "50%"}),

    html.Label("📈 Market Value (ETH):", style={"font-weight": "bold", "margin-top": "10px"}),
    dcc.RangeSlider(id="market_value_slider", min=market_value_min, max=market_value_max, step=0.01,
                    value=[market_value_min, market_value_max],
                    marks={int(market_value_min): f"{market_value_min:.2f} ETH",
                           int(market_value_max): f"{market_value_max:.2f} ETH"}),

    html.Label("💰 Floor Price (ETH):", style={"font-weight": "bold", "margin-top": "10px"}),
    dcc.RangeSlider(id="floor_price_slider", min=floor_price_min, max=floor_price_max, step=0.01,
                    value=[floor_price_min, floor_price_max],
                    marks={int(floor_price_min): f"{floor_price_min:.2f} ETH",
                           int(floor_price_max): f"{floor_price_max:.2f} ETH"}),

    html.Label("👥 Number of Owners:", style={"font-weight": "bold", "margin-top": "10px"}),
    dcc.Slider(id="owners_slider", min=owners_min, max=owners_max, step=10,
               value=owners_max // 2,
               marks={int(owners_min): f"{owners_min}", int(owners_max): f"{owners_max}"}),

    html.Label("🔄 Sales Volume:", style={"font-weight": "bold", "margin-top": "10px"}),
    dcc.Slider(id="sales_slider", min=sales_min, max=sales_max, step=10,
               value=sales_max // 2,
               marks={int(sales_min): f"{sales_min}", int(sales_max): f"{sales_max}"}),

    html.Label("📅 Collection Age (Days):", style={"font-weight": "bold", "margin-top": "10px"}),
    dcc.RangeSlider(id="collection_age_slider", min=int(age_min), max=int(age_max), step=10,
                    value=[int(age_min), int(age_max)],
                    marks={int(age_min): f"{age_min} Days", int(age_max): f"{age_max} Days"}),

], style={"margin-bottom": "20px"})

# 📌 Default Graph
default_graph = px.bar(
    df.nlargest(10, "avg_market_value"),
    x="name",
    y="avg_market_value",
    title="Top 10 NFT Collections by Market Value",
    labels={"name": "NFT Collection", "avg_market_value": "Market Value (ETH)"},
    color="avg_market_value",
    height=550
)

# 📌 Layout with Dynamic Description
layout = html.Div([
    html.H1("NFT Collection Analysis", style={"text-align": "center"}),

    html.P("Use the filters below to analyze different types of NFT collections.", style={"text-align": "center"}),

    html.Div(id="category_description", style={"font-size": "18px", "margin": "20px", "color": "#555"}),  # 📌 Dynamic Description

    filters_layout,

    dcc.Graph(id="filtered_nft_graph", figure=default_graph)],

    className="nft-collections-page")

# 📌 Register Callbacks
def register_callbacks(app):
    @app.callback(
        [Output("filtered_nft_graph", "figure"),
         Output("category_description", "children")],
        [Input("nft_category_dropdown", "value"),
         Input("market_value_slider", "value"),
         Input("floor_price_slider", "value"),
         Input("owners_slider", "value"),
         Input("sales_slider", "value"),
         Input("collection_age_slider", "value")]
    )
    def update_filtered_graph(category, market_range, floor_range, owners, sales, age_range):
        # Apply filters to the dataset dynamically
        filtered_df = df[
            (df["category"] == category) &
            (df["avg_market_value"].between(market_range[0], market_range[1])) &
            (df["floor_price"].between(floor_range[0], floor_range[1])) &
            (df["num_owners"] >= owners) &
            (df["transfers_count"] >= sales) &
            (df["collection_age"].between(age_range[0], age_range[1]))
        ].nlargest(10, "avg_market_value")

        fig = px.bar(filtered_df, x="name", y="avg_market_value",
                     title=f"Top 10 {category} NFTs by Market Value",
                     color="avg_market_value", height=550)

        description = category_descriptions.get(category, "No description available.")
        return fig, description
