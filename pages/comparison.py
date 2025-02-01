from dash import html, dcc, Input, Output 
import plotly.express as px
import pandas as pd
import numpy as np

# 📌 Simulated Data for NFT Collections (Replace with real data if available)
nft_data = {
    "MutantApeYachtClub": pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
        "Market Value": np.random.randint(20, 100, 12),
    }),
    "BoredApeKennelClub": pd.DataFrame({
        "Category": np.random.choice(["Low", "Mid", "High", "Premium"], 50),
        "Market Value": np.random.randint(5, 100, 50),
    }),
    "Neon Junkies": pd.DataFrame({
        "Owners": np.random.randint(10, 5000, 15),
        "Trading Activity": np.random.randint(1, 200, 15),
        "Size": np.random.randint(10, 100, 15),
    }),
    "CryptoPunks": pd.DataFrame({
        "Rarity": ["Common", "Uncommon", "Rare", "Legendary"],
        "Price (ETH)": np.random.randint(50, 500, 4),
        "Color": ["blue", "green", "orange", "red"]
    }),
    "Azuki": pd.DataFrame({
        "Floor Price": np.random.randint(5, 50, 50),
        "Collection": ["Azuki"] * 50
    })
}

# 📌 Dropdown for NFT Selection
dropdown = dcc.Dropdown(
    id="collection_dropdown",
    options=[{"label": name, "value": name} for name in nft_data.keys()],
    value="MutantApeYachtClub",
    clearable=False,
    style={"background-color": "#ffffff", "color": "black"}
)

# 📌 Layout with extra bottom padding for better readability
layout = html.Div(
    className="comparison-page",  # Added for CSS styling
    children=[
        html.H1("Compare NFT Collections"),

        html.P(
            "Use the dropdown to compare different NFT collections based on their market value, trading activity, and ownership trends.",
            style={"font-size": "16px", "color": "#ffffff"}
        ),

        dropdown,

        # 📌 Graph Display
        dcc.Graph(id="comparison_graph", style={"margin-top": "20px"}),

        # 📌 Description Section with extra bottom padding
        html.Div(
            id="graph_description",
            style={
                "font-size": "18px",
                "color": "#ffffff",
                "margin-top": "20px",
                "padding-bottom": "100px",  # Adds extra scrolling space
            }
        )
    ]
)

# 📌 Callback for Updating Graph & Description
def register_callbacks(app):
    @app.callback(
        [Output("comparison_graph", "figure"), Output("graph_description", "children")],
        Input("collection_dropdown", "value")
    )
    def update_graph_and_description(selected_name):
        df = nft_data[selected_name]

        if selected_name == "MutantApeYachtClub":
            fig = px.area(df, x="Date", y="Market Value", title="Market Value Growth Over Time", color_discrete_sequence=["#1f77b4"])
            description = """
            📌 "Mutant Ape Yacht Club (MAYC)" shows a Steady Upward Trend in market value, as represented in the area chart.  
            A Gradual increase suggests a Strong Investor Base and Sustained Demand.  
            Any dips indicate periods of "high trading activity or market corrections".  
            Investors looking for long-term returns might find MAYC a strong choice.  
            """

        elif selected_name == "BoredApeKennelClub":
            fig = px.box(df, x="Category", y="Market Value", title="Market Value Distribution Across Categories", color="Category")
            description = """
            📌 "Bored Ape Kennel Club (BAKC)" exhibits "market variations" across different categories.  
            Premium category has a Higher Median Value, while Low and Mid categories show fluctuations.  
            Outliers indicate rare, high-value sales, signaling demand for specific traits.  
            Investment strategy: Budget investors may opt for Low/Mid tiers, while High/Premium buyers seek exclusivity.  
            """

        elif selected_name == "Neon Junkies":
            fig = px.scatter(df, x="Owners", y="Trading Activity", size="Size", title="Trading Activity vs. Number of Owners", color_discrete_sequence=["#ff7f0e"])
            description = """
            📌 "Neon Junkies" is an Emerging NFT collection with "high variance in trading activity", as seen in the Bubble chart.  
            X-Axis: Represents the number of unique NFT holders.  
            Y-Axis: Shows frequency of trades.  
            Bubble Size: Indicates the market size of each group.  
            Key Takeaway: If larger bubbles cluster at "higher ownership levels", it suggests Widespread Adoption and Liquidity.  
            """

        elif selected_name == "CryptoPunks":
            fig = px.bar(df, x="Rarity", y="Price (ETH)", title="Price Distribution by Rarity", color="Color", text_auto=True)
            description = """
            📌 "CryptoPunks" has a well-defined "rarity-based pricing" model, visualized in the Bar chart.  
            Common vs. Legendary: Common NFTs are priced significantly lower, while Legendary Punks have the highest value.  
            Stepwise increase: Uncommon and Rare categories show "clear price segmentation".  
            Investment Insight: Buyers seeking Low-risk Entry Points can look at Uncommon NFTs, while Rare & Legendary appeal to long-term investors.  
            """

        elif selected_name == "Azuki":
            fig = px.violin(df, y="Floor Price", box=True, points="all", title="Floor Price Spread of Azuki Collection", color_discrete_sequence=["#d62728"])
            description = """
            📌 "Azuki NFTs" exhibit "Significant Price Variation", as seen in the Violin plot.  
            Wider sections indicate where most sales are happening.  
            The box plot inside provides median and quartile values, showing "price stability".  
            Outliers (dots) represent "occasional high-value sales", suggesting some Azuki NFTs are Extremely Valuable.  
            Investor Perspective: If investing in Azuki, understanding price trends is Key to Maximizing Returns.  
            """

        return fig, description
