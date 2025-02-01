from dash import Input, Output
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load cleaned dataset
file_path = "data/nfts_cleaned.csv"  # Ensure the CSV file is inside the 'data' folder
df = pd.read_csv(file_path)

# Apply K-Means clustering (already cleaned dataset)
kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(df[["avg_market_value", "num_owners", "transfers_count"]])

# Apply PCA for clustering visualization
pca = PCA(n_components=2)
df_pca = pca.fit_transform(df[["avg_market_value", "num_owners", "transfers_count"]])
df["pca_1"], df["pca_2"] = df_pca[:, 0], df_pca[:, 1]

# Define callbacks
def register_callbacks(app):
    @app.callback(
        Output("scatter_plot", "figure"),
        Input("cluster_dropdown", "value"),
    )
    def update_scatter_plot(cluster):
        filtered_df = df[df["cluster"] == cluster]
        fig = px.scatter(
            filtered_df,
            x="num_owners",
            y="avg_market_value",
            color="cluster",
            title="Market Value vs. Owners (Filtered by Cluster)",
            labels={"num_owners": "Number of Owners", "avg_market_value": "Market Value"},
        )
        return fig

    @app.callback(
        Output("cluster_plot", "figure"),
        Input("cluster_dropdown", "value"),
    )
    def update_cluster_plot(cluster):
        filtered_df = df[df["cluster"] == cluster]
        fig = px.scatter(
            filtered_df,
            x="pca_1",
            y="pca_2",
            color="cluster",
            title="Cluster Visualization (PCA)",
            labels={"pca_1": "PCA Component 1", "pca_2": "PCA Component 2"},
        )
        return fig
