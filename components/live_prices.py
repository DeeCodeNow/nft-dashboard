import requests
import pandas as pd
from dash import dcc, html, Input, Output

# 📌 Fetch Real-Time NFT Prices from OpenSea API
def get_live_nft_prices():
    url = "https://api.opensea.io/api/v1/assets"
    params = {
        "order_direction": "desc",
        "limit": 5,  # Fetch top 5 trending NFTs
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        assets = response.json().get("assets", [])
        data = []
        for asset in assets:
            data.append({
                "name": asset["name"] if asset["name"] else "Unknown NFT",
                "price": asset["last_sale"]["total_price"] if asset.get("last_sale") else "N/A",
                "image": asset["image_url"] if asset["image_url"] else "https://via.placeholder.com/150",
            })
        return pd.DataFrame(data)
    else:
        print("⚠️ OpenSea API Error:", response.status_code)
        return pd.DataFrame(columns=["name", "price", "image"])

# 📌 Live NFT Price Tracker Component
def live_nft_price_component():
    df = get_live_nft_prices()
    
    return html.Div([
        html.H3("🔥 Live NFT Prices (From OpenSea)"),
        html.Div([
            html.Div([
                html.Img(src=row["image"], style={"width": "100px", "border-radius": "10px"}),
                html.P(f"{row['name']} - {row['price'][:5]} ETH" if row["price"] != "N/A" else f"{row['name']} - N/A")
            ], style={"display": "inline-block", "padding": "10px"}) for _, row in df.iterrows()
        ], style={"display": "flex", "overflowX": "scroll"})
    ])
