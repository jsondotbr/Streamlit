import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(page_title="AI Platforms Status Dashboard", layout="wide")

# Auto-refresh every 5 minutes (300000 ms)
st_autorefresh = st.experimental_autorefresh(interval=300000, limit=None, key="refresh")

# Function to fetch status
def fetch_status():
    platforms = {
        "OpenAI": "https://status.openai.com/api/v2/status.json",
        "Anthropic": "https://status.anthropic.com/api/v2/status.json",
        "Cohere": "https://status.cohere.ai/api/v2/status.json",
        "Hugging Face": "https://status.huggingface.co/api/v2/status.json",
        "GitHub Copilot": "https://www.githubstatus.com/api/v2/status.json"
    }

    data = []
    for name, url in platforms.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                status_info = response.json().get("status", {})
                indicator = status_info.get("indicator", "unknown")
                description = status_info.get("description", "No description")
            else:
                indicator = "unknown"
                description = "Failed to fetch"
        except Exception as e:
            indicator = "unknown"
            description = str(e)

        # Map indicator to color and readable status
        if indicator == "none":
            color = "green"
            readable_status = "Operational"
        elif indicator == "minor":
            color = "yellow"
            readable_status = "Partial Outage"
        elif indicator == "major":
            color = "red"
            readable_status = "Major Outage"
        else:
            color = "gray"
            readable_status = "Unknown"

        data.append({
            "Platform": name,
            "Status": readable_status,
            "Color": color,
            "Description": description,
            "Last Updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        })

    return pd.DataFrame(data)

# Title
st.title("AI Platforms Status Dashboard")
st.write(f"Auto-refresh every 5 minutes. Last refreshed at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

# Fetch and display data
df = fetch_status()

# Apply color coding
def color_status(val):
    if val == "Operational":
        return "background-color: green; color: white;"
    elif val == "Partial Outage":
        return "background-color: yellow; color: black;"
    elif val == "Major Outage":
        return "background-color: red; color: white;"
    else:
        return "background-color: gray; color: white;"

st.dataframe(df.style.applymap(color_status, subset=["Status"]))
