import streamlit as st
from streamlit_folium import st_folium
import folium
import time
from geopy.distance import geodesic

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="AI Traffic Light Simulation", layout="wide")
st.title("🚦 4-Way Traffic Light Simulation for Ambulance (East → West)")

# Intersection center
intersection = (13.0837, 80.2727)

# Define 4 traffic signals
traffic_lights = [
    {"direction": "North", "location": (intersection[0] + 0.001, intersection[1]), "status": "Red"},
    {"direction": "South", "location": (intersection[0] - 0.001, intersection[1]), "status": "Red"},
    {"direction": "East",  "location": (intersection[0], intersection[1] + 0.001), "status": "Red"},
    {"direction": "West",  "location": (intersection[0], intersection[1] - 0.001), "status": "Red"}
]

# Ambulance route: East (home) → Intersection → West (hospital)
ambulance_route = [
    (13.0837, 80.2760),   # Far East (home)
    (13.0837, 80.2750),
    (13.0837, 80.2740),
    (13.0837, 80.2730),
    (13.0837, 80.2727),   # Intersection
    (13.0837, 80.2720),
    (13.0837, 80.2710),   # West side (hospital)
]

# ----------------------------
# FUNCTIONS
# ----------------------------
def is_near(ambulance, signal, threshold=0.2):
    """Return True if ambulance is within threshold (km) ~ 200m."""
    return geodesic(ambulance, signal).km <= threshold

def update_lights(current_location, has_crossed=False):
    """Update traffic lights so only East is Green when ambulance approaches."""
    logs = []
    for light in traffic_lights:
        if light["direction"] == "East" and not has_crossed:
            if is_near(current_location, light["location"], threshold=0.2):  # 200m
                light["status"] = "Green"
                logs.append("East signal set to GREEN (ambulance approaching).")
            else:
                light["status"] = "Red"
                logs.append("East signal is RED (ambulance still far).")
        else:
            light["status"] = "Red"
            if light["direction"] != "East":
                logs.append(f"{light['direction']} signal set to RED.")
    return logs

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("AI Agent Dashboard")
status_placeholder = st.sidebar.empty()
reasoning_placeholder = st.sidebar.empty()
st.sidebar.markdown("---")
auto_run = st.sidebar.checkbox("Auto-Run Simulation", value=True)

# ----------------------------
# MAIN SIMULATION
# ----------------------------
has_crossed = False
for idx, location in enumerate(ambulance_route):
    status_placeholder.info(f"Processing ambulance position {idx+1}/{len(ambulance_route)}...")
    time.sleep(1)

    # Mark as crossed after ambulance passes the intersection
    if location == intersection:
        has_crossed = True

    # Update traffic light decisions
    ai_logs = update_lights(location, has_crossed)

    # Show reasoning
    reasoning_placeholder.empty()
    reasoning_placeholder.subheader("AI Reasoning")
    for log in ai_logs:
        reasoning_placeholder.write(f"- {log}")
        time.sleep(0.3)

    # Map
    m = folium.Map(location=location, zoom_start=17)

    # Draw intersection roads
    folium.PolyLine([(intersection[0] + 0.002, intersection[1]), (intersection[0] - 0.002, intersection[1])],
                    color="gray", weight=4, opacity=0.5).add_to(m)
    folium.PolyLine([(intersection[0], intersection[1] + 0.002), (intersection[0], intersection[1] - 0.002)],
                    color="gray", weight=4, opacity=0.5).add_to(m)

    # Ambulance route
    folium.PolyLine(ambulance_route, color="blue", weight=5, opacity=0.7).add_to(m)

    # Ambulance marker
    folium.Marker(location, popup="Ambulance",
                  icon=folium.Icon(color="blue", icon="ambulance", prefix="fa")).add_to(m)

    # Signals
    for light in traffic_lights:
        folium.Marker(
            light["location"],
            popup=f"{light['direction']} Signal: {light['status']}",
            icon=folium.Icon(
                color="green" if light["status"] == "Green" else "red",
                icon="traffic-light",
                prefix="fa"
            )
        ).add_to(m)

    st_folium(m, width=900, height=500)

    if not auto_run:
        break
    if idx < len(ambulance_route) - 1:
        time.sleep(2)

# ----------------------------
# END
# ----------------------------
if auto_run:
    st.sidebar.success("Ambulance has cleared the East signal and reached the hospital safely!")
st.markdown("---")
st.markdown("**Hackathon Demo:** 4-Way Traffic Light (East → West Route with Predictive Green Signal)**")
