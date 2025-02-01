import sys
import os
import pytest
from app import app
from pages import home, insights, trends, comparison, data_insights, nft_collections

# ✅ Ensure the app directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Pytest fixture for Dash test client
@pytest.fixture
def client():
    return app.server.test_client()

# ✅ Test: Ensure the app runs and the home page loads
def test_app_starts(client):
    response = client.get("/")
    assert response.status_code == 200, "Home page failed to load"

# ✅ Test: Ensure all pages load correctly
@pytest.mark.parametrize("route", ["/", "/insights", "/trends", "/comparison", "/data_insights", "/nft_collections"])
def test_page_routes(client, route):
    response = client.get(route)
    assert response.status_code == 200, f"Page {route} failed to load"

# ✅ Test: Ensure navigation links exist
def test_nav_links_exist():
    nav_items = ["Home", "Insights", "Trends", "Compare", "Market Insights", "NFT Collections"]
    rendered_html = str(app.layout)
    for item in nav_items:
        assert item in rendered_html, f"Navigation link '{item}' missing"

# ✅ Test: Ensure comparison page dropdown exists (Fetching dynamically)
def test_comparison_dropdown():
    assert "collection_dropdown" in str(comparison.layout), "Comparison dropdown missing"

# ✅ Test: Ensure trends page dropdown exists (Fetching dynamically)
def test_trends_dropdown():
    assert "metric_dropdown" in str(trends.layout), "Trends dropdown missing"

# ✅ Test: Ensure trends graph exists (Fetching dynamically)
def test_trends_graph_update():
    assert "trend_graph" in str(trends.layout), "Trends graph missing"

# ✅ Test: Ensure NFT collections filters exist (Fetching dynamically)
def test_nft_collections_filters():
    filters = ["market_value_slider", "floor_price_slider", "owners_slider"]
    rendered_html = str(nft_collections.layout)
    for f in filters:
        assert f in rendered_html, f"Filter '{f}' missing in NFT collections page"

# ✅ Test: Ensure footer exists (Fetching dynamically)
def test_footer_exists():
    assert "Built with Dash & Plotly" in str(home.layout), "Footer text missing"

# ✅ Test: Ensure home page title exists (Fetching dynamically)
def test_home_title_exists():
    assert "Welcome to the NFT Dashboard" in str(home.layout), "Home page title missing"

# ❌ **Allowed Failed Case 1**: Test an invalid URL (Expected Fix: Redirect instead of 404)
def test_invalid_page(client):
    response = client.get("/invalidpage")
    assert response.status_code in [200, 302], "Expected redirect to home or 404"

# ❌ **Allowed Failed Case 2**: Ensure the app title is correct (Intentional Failure)
def test_app_title():
    expected_title = "NFT Dashboard"  # ❌ This will fail since the title is "NFT Market Dashboard"
    actual_title = app.title
    assert actual_title == expected_title, f"App title mismatch: Expected '{expected_title}', got '{actual_title}'"
