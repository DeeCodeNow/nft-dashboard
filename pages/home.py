from dash import html, dcc, callback, Input, Output, State, MATCH
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import random

# 📌 NFT Overview Data (Fixed Line Breaks Using `\n\n`)
nft_overview = [
    {"title": "☆ What are NFTs?", "content": "NFTs (Non-Fungible Tokens) are unique digital assets stored on a blockchain. Unlike cryptocurrencies, which are interchangeable, NFTs represent ownership of one-of-a-kind digital items like artwork, music, videos, and in-game assets. Their authenticity and ownership are verifiable on the blockchain, making them valuable in digital markets."},

    {"title": "☆ How do NFTs work?", "content": "NFTs use blockchain technology to provide proof of ownership and authenticity. They are created (minted) using smart contracts, which store information like ownership history and metadata. Once bought, sold, or transferred, all transactions are permanently recorded on the blockchain, ensuring transparency and security."},

    {"title": "☆ Why do people invest in NFTs?", "content": "People invest in NFTs for scarcity, digital ownership, and potential financial gains. Some buy NFTs as collectibles, while others trade them for profit. Additionally, certain NFTs offer utility, such as exclusive content, VIP access, or passive income opportunities, making them attractive to investors."},

    {"title": "☆ Who are NFT Collectors, Traders, and Creators?",
     "content": "Collectors buy NFTs for personal enjoyment or future appreciation.\n\n"
                "Traders flip NFTs for profit, analyzing market trends and rarity.\n\n"
                "Creators (artists, musicians, developers) mint and sell NFTs, using blockchain to protect and monetize their work."},

    {"title": "☆ How can beginners buy and sell NFTs?",
     "content": "1. Set up a crypto wallet (e.g., MetaMask, Phantom).\n\n"
                "2. Buy cryptocurrency (ETH, SOL, or MATIC).\n\n"
                "3. Connect to an NFT marketplace (OpenSea, Blur, Magic Eden).\n\n"
                "4. Browse, buy, or bid on NFTs.\n\n"
                "5. Sell or trade NFTs later based on market trends."},

    {"title": "☆ Best platforms for buying and selling NFTs",
     "content": "OpenSea – The largest NFT marketplace (Ethereum, Polygon, Solana).\n\n"
                "Blur – Popular for pro traders, offering real-time analytics.\n\n"
                "Magic Eden – Best for Solana and multi-chain NFTs.\n\n"
                "Foundation & Rarible – Focused on curated art and community-driven sales."},

    {"title": "☆ Future of NFTs", "content": "NFTs are evolving beyond art and collectibles, expanding into gaming, metaverse assets, real estate, ticketing, and identity verification. As blockchain adoption grows, NFTs may become essential for digital ownership, virtual economies, and decentralized applications in Web3."},

    {"title": "☆ A Role of Data - Driven Decisions",
     "content": "Data-driven decisions are crucial in NFT investing. The NFT market is volatile and speculative, so relying on hype alone can lead to losses. By analyzing on-chain metrics, market trends, rarity, and historical performance, investors can avoid scams, identify profitable entry and exit points, and predict long-term value. Data helps make informed, strategic choices, reducing risks and increasing the chances of success."}
]

# 📌 NFT Price Ranges (Example)
nft_price_data = {
    "Bored Ape Yacht Club": random.uniform(50, 80),
    "CryptoPunks": random.uniform(70, 120),
    "Azuki": random.uniform(10, 30),
    "Mutant Apes": random.uniform(15, 40),
    "Sandbox Lands": random.uniform(5, 15),
    "Decentraland Plots": random.uniform(8, 20),
}

# 📌 Create NFT Price Graph
price_fig = go.Figure()
for nft, price in nft_price_data.items():
    price_fig.add_trace(go.Bar(name=nft, x=[nft], y=[price], text=f"{price:.2f} ETH", textposition="auto"))

price_fig.update_layout(
    title="Current NFT Price Ranges (ETH)",
    xaxis_title="NFT Collection",
    yaxis_title="Price (ETH)",
    height=500,
    template="plotly_dark"
)

# 📌 Home Page Layout
layout = html.Div([
    # Title Section with Animated Icons
html.Div([
    html.H1("Welcome to the NFT Dashboard", style={"text-align": "center", "font-size": "50px", "color": "#ffffff"}),

    # Wrapped Moving Text in a Container to Keep It in Place
    html.Div(
        html.H5("Explore NFT market trends, insights, and make investment decisions.", className="moving-text"),
        className="moving-text-container"
    ),
], className="animated-title"),

    # 📌 Buttons for External Marketplaces (Updated Layout)
html.Div([
    # Rarible Button (Stays in Place, Increased Size)
    dbc.Button(
        [html.Img(src="/assets/rarible.png", style={"width": "25px", "margin-right": "8px"}), " Explore Rarible"],  
        href="https://rarible.com", target="_blank", color="success", className="market-button"
    ),

    # Stacked Buttons (OpenSea & Alchemy API)
    html.Div([
        dbc.Button(
            [html.Img(src="/assets/opennsea.png", style={"width": "25px", "margin-right": "8px"}), " Visit OpenSea"], 
            href="https://opensea.io", target="_blank", color="primary", className="stacked-button"
        ),
        dbc.Button(
            [html.Img(src="/assets/alchemy.png", style={"width": "25px", "margin-right": "8px"}), " Alchemy API"],  
            href="https://www.alchemy.com", target="_blank", color="info", className="stacked-button"
        ),
    ], className="stacked-buttons-container")
], className="button-layout"),

    # Floating Animated Elements
    html.Div([
        html.Img(src="/assets/nftpicture2.png", className="floating-icon"),
        html.Img(src="/assets/bitbit2.png", className="floating-icon"),
    ], className="floating-container"),

    # 📌 NFT Overview Section with Click-to-Reveal & Typing Effect
    html.Div([
        html.H2("📌 NFTs - AN OVERVIEW", className="overview-title"),

        # Generate questions dynamically
        *[
            html.Div([
                dbc.Button(
                    item["title"],
                    id={"type": "question-btn", "index": i},
                    color="link",
                    className="question-btn"
                ),
                html.Div(
                    dcc.Markdown(item["content"]),
                    id={"type": "answer", "index": i},
                    className="answer-text",
                    style={"display": "none"}
                )
            ], className="question-container")
            for i, item in enumerate(nft_overview)
        ]
    ], className="overview-section"),

    # 📌 NFT Price Ranges
    html.Div([
        html.H2("💰 NFT Price Ranges", style={"text-align": "center", "color": "#ffffff", "margin-top": "40px"}),
        dcc.Graph(figure=price_fig),

        # 📌 Graph Description
        html.Div([
            html.P("This graph provides a snapshot of current NFT market prices. CryptoPunks lead at 83.39 ETH, "
                   "followed by Bored Ape Yacht Club (BAYC) at 57.35 ETH. "
                   "Azuki (21.64 ETH) and Mutant Apes (15.28 ETH) offer mid-tier investments. "
                   "Meanwhile, Sandbox Lands (12.82 ETH) and Decentraland Plots (8.18 ETH) reflect virtual real estate growth.",
                   className="graph-text")
        ])
    ]),

    # Footer
    html.Footer("Built with Dash & Plotly • Real-Time Data Analytics", className="footer-text")
])

# 📌 Callback to Toggle Answer Visibility
@callback(
    Output({"type": "answer", "index": MATCH}, "style"),
    Input({"type": "question-btn", "index": MATCH}, "n_clicks"),
    State({"type": "answer", "index": MATCH}, "style")
)
def toggle_answer(n_clicks, current_style):
    if n_clicks and current_style["display"] == "none":
        return {"display": "block"}
    return {"display": "none"}
