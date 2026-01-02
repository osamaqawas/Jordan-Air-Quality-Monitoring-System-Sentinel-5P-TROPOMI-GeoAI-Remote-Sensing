[Readme.txt](https://github.com/user-attachments/files/24407160/Readme.txt)
🛰️ Jordan Air Quality Monitoring System Sentinel-5P (TROPOMI)  GeoAI & Remote Sensing

An advanced GeoAI-powered web application for monitoring and analyzing atmospheric air pollutants over Jordan, with a special focus on Irbid and major urban centers. The platform utilizes Sentinel-5P (TROPOMI) satellite data and Google Earth Engine to provide spatio-temporal insights into air quality patterns from 2019 to the present.

🌍 Project Overview

Air pollution poses significant environmental and public health challenges in Jordan due to urban expansion, traffic emissions, industrial activity, and natural dust events. This application enables interactive visualization, analysis, and reporting of key air quality indicators using satellite-based observations.

🚀 Key Features

Multi-Pollutant Monitoring

Nitrogen Dioxide (NO₂)

Sulfur Dioxide (SO₂)

Carbon Monoxide (CO)

Aerosol Index (Dust & Smoke)

Temporal Analysis

Monthly and yearly filtering (2019–present)

Seasonal variation assessment

Interactive Geospatial Visualization

Dynamic maps powered by Geemap and Google Earth Engine

High-level satellite data processing in real time

City-Based Statistics

Extract mean pollutant values for major Jordanian cities

Export results as CSV reports

Scientific Interpretation

Contextual explanations linking pollutants to their main emission sources

🛠️ Technology Stack

Backend & Processing Google Earth Engine (GEE) Python API

Frontend Streamlit

Geospatial Visualization Geemap & Folium

Satellite Data Source ESA Sentinel-5P (TROPOMI)

📊 Data Source

Satellite Sentinel-5P

Sensor TROPOMI (Tropospheric Monitoring Instrument)

Agency European Space Agency (ESA)

Spatial Resolution ~7 × 3.5 km

Products Level-3 Atmospheric Composition Data

📖 Scientific Context

This project is part of an ongoing research initiative at Yarmouk University, conducted in collaboration with the Spanish Ministry of Science, Innovation, and Universities. The study integrates remote sensing, geospatial analysis, and AI-driven approaches to assess environmental impacts related to

Urban growth

Traffic emissions

Industrial activity

Natural dust transport

⚙️ Installation & Setup 1️⃣ Clone the Repository git clone httpsgithub.comYOUR_USERNAMEJordan-AirQuality-Sentinel5P.git cd Jordan-AirQuality-Sentinel5P

2️⃣ Install Dependencies pip install -r requirements.txt

3️⃣ Configure Google Earth Engine

Create a service account

Add credentials to

.streamlitsecrets.toml

Example

GEE_JSON = { type service_account, ... }

4️⃣ Run the Application streamlit run app.py

📤 Outputs

Interactive air quality maps

City-based statistical tables

Downloadable CSV reports

Scientific interpretations for each pollutant

📌 Use Cases

Environmental monitoring & research

Urban air quality assessment

Academic demonstrations

Decision support for environmental studies

🤝 Acknowledgments

European Space Agency (ESA) – Sentinel-5P data

Google Earth Engine – Cloud-based geospatial processing

Yarmouk University – Academic and research support

📫 Contact

For collaboration, research inquiries, or feedback, feel free to connect via LinkedIn or GitHub.
