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
def get_new_data():
    if strategy_type == "CACHE_FIRST":
        try:
            response = requests.get("http://localhost:5000/cache_first_stats")
            json_data = response.json()
            labels = ['Hits', 'Misses']
            values = [json_data['hits'], json_data['misses']]
        except Exception as e:
            print(e)
            labels = ['Hits', 'Misses']
            values = [0, 0]
    return labels, values


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
    labels, values = get_new_data()

    # Plot the pie chart with updated data
    fig = plot_pie_chart(labels, values)
    st.plotly_chart(fig)

    # Delay for 2 seconds before the next update
    time.sleep(2)
    st.rerun()


