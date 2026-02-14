# SWROS – Smart Waste & Resource Optimization System

## About
SWROS is a full-stack web application built during a 30-hour hackathon focused on Smart Tech for Industry 5.0.

The project explores how software can help industries detect, visualize, and understand hidden inefficiencies—such as water leaks, declining machine performance, and invisible waste—before they turn into major losses.

This is a working prototype designed to demonstrate ideas, logic, and system thinking under real time constraints.

---

## What the System Does

### Smart Water Leakage Detection
- Interactive pipe network builder
- Add, connect, and delete nodes visually
- Monitor pressure values at each node
- Automatically detect leaks based on pressure drop thresholds
- Highlight leaks directly on the network
- Save and reload network state using JSON
- One-click fixing of individual or all leaks

---

### Machine Health Monitoring
- Analyze machine performance using batch-level data
- Compare input, output, waste, and energy consumption
- Calculate efficiency scores and waste ratios
- Flag machines as healthy or faulty
- Suggest repair actions when thresholds are crossed

---

### Invisible Waste Tracking
- Calculate invisible waste using:
  input − output − recorded waste
- Identify high-loss batches
- Estimate cost impact
- Visualize trends by machine, shift, and batch
- Provide quick KPIs and detailed tables

---

## How It’s Built
- Backend: Python, Flask, Pandas
- Frontend: HTML, CSS, JavaScript
- Charts: Chart.js
- Network Visualization: Cytoscape.js
- Data Formats: CSV, JSON

The system is intentionally software-driven and does not rely on hardware or IoT integration.

---

## Project Structure

SWROS/
├── app.py
├── data/
│   ├── production_data.csv
│   ├── machine_health.json
│   └── network.json
├── templates/
│   ├── home.html
│   ├── invisible_waste.html
│   ├── machine_health.html
│   └── water_network.html
└── README.md

---

## Running the Project Locally

pip install flask pandas
python app.py

Then open your browser and go to:
http://127.0.0.1:5000

---

## Team
Built during the hackathon by Team Byte404:
- Sooraj Kumar S
- Lizona Loy Parayil
- Ryan Sebastian
- Devananda A

---

## Future Improvements
- Code refactoring and modularization
- Alerts and notification system
- Integration with real sensor data
- Cloud deployment
- Advanced analytics and predictive maintenance

---

## Notes
This project was built under strict time constraints during a hackathon and is intended for educational and demonstration purposes.
