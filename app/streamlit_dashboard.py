from dotenv import load_dotenv
import os
import requests
import streamlit as st
import plotly.graph_objects as go
import time

# get the environment variable for the cache strategy
load_dotenv()
strategy_type = os.getenv("CACHE_STRATEGY")
colors = ["#a30b00", "#007a27", "#1726ff"]

# Title of the page
st.title(f"Web caching strategies: {strategy_type}")

# Layout Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #2e2e2e;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            font-size: 18px;
        }
        .stText {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# Simulate real-time data (e.g., hits vs. misses)
def get_new_data_cache_first():
    try:
        response = requests.get("http://localhost:5000/cache_first_stats")
        json_data = response.json()
        labels = ['Hits', 'Misses']
        values = [json_data['hits'], json_data['misses']]
    except Exception as e:
        labels = ['Hits', 'Misses']
        values = [0, 0]
    return labels, values


# Simulate real-time data (e.g., Updates and latency)
def get_new_data_network_first():
    try:
        response = requests.get("http://localhost:5000/network_first_stats")
        json_data = response.json()
    except Exception as e:
        json_data = {
            "updates": 0,
            "latency_network": []
        }
    return json_data

# Simulate real-time data (e.g., Misses, Hits and latency)
def get_new_data_stale_while_revalidate():
    try:
        response = requests.get("http://localhost:5000/stale_while_revalidate_stats")
        json_data = response.json()
    except Exception as e:
        json_data = {
            "Hits": 0,
            "Misses": 0,
            "latency_network": []
        }
    return json_data


# Pie chart visualization
def plot_pie_chart(labels, values):
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,  # Donut chart
        marker=dict(colors=["#00bfae", "#ff6f61"]),
        textinfo='label+percent',
        insidetextorientation='radial'
    )])

    fig.update_layout(
        title="Hits vs Misses",
        title_x=0.5,
        margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins
        paper_bgcolor="#575757",  # Background color
        plot_bgcolor="#424242",  # Chart background
        autosize=True,  # Ensures responsiveness
    )

    return fig


while True:
    # Plot the pie chart with updated data
    if strategy_type == "CACHE_FIRST":
        labels, values = get_new_data_cache_first()
        fig = plot_pie_chart(labels, values)
        st.plotly_chart(fig)
    elif strategy_type == "NETWORK_FIRST":
        stats = get_new_data_network_first()
        total_updates = stats.get("updates", 0)
        latencies = stats.get("latency_network", [])
        same_as_in_cache = stats.get("same_as_in_cache_counts", 0)
        avg_latency = round(sum(latencies) / len(latencies), 3) if latencies else 0

        st.subheader("Network-First Strategy Metrics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Total Updates", value=total_updates)

        with col2:
            st.metric(label="Average Latency (s)", value=avg_latency)

        with col3:
            st.metric(label="Cache data same as in network", value=same_as_in_cache)
    else:
        stats = get_new_data_stale_while_revalidate()
        labels, values = ["Hits", "Misses"], [stats["hits"], stats["misses"]]
        latency_stales = stats.get("latency_stale", [])
        latency_misses = stats.get("latency_misses", [])
        total_updates = stats.get("updates", 0)

        fig = plot_pie_chart(labels, values)
        st.plotly_chart(fig)

        avg_latency_stales = sum(latency_stales) / len(latency_stales) if latency_stales else 0
        avg_latency_misses = sum(latency_misses) / len(latency_misses) if latency_misses else 0

        st.subheader("Stale while revalidate")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Total Updates", value=total_updates)
        with col2:
            st.metric(label="Average latency stales", value=avg_latency_stales)
        with col3:
            st.metric(label="Average latency misses", value=avg_latency_misses)

    # Delay for 2 seconds before the next update
    time.sleep(2)
    st.rerun()


