# Ambulance-AI-traffic-simulation
AI-powered traffic light system that creates real-time green corridors for ambulances using GPS tracking and smart signal control.

 Problem
- Ambulances are delayed in heavy urban traffic.
- Fixed signal timers do not adapt to emergencies.
- 4-way intersections often block ambulances due to lack of priority.

 Solution
- Real-time GPS tracking of ambulances.  
- AI agent predicts ambulance route and clears signals ahead of time.  
- At intersections, AI sets ambulance path to GREEM and other paths to RED  
- Interactive dashboard built with Streamlit and Folium for live visualization.  

Tech Stack
- Frontend: Streamlit, Folium  
- Backend: Python  
- AI Logic: Geopy (distance calculation), rule-based AI  
- Visualization: Interactive maps & reasoning logs  
- IoT Ready:Can integrate with smart traffic controllers  

Run Locally
cd ambulance-ai-traffic
pip install -r requirements.txt
python -m streamlit run app.py
