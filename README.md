# Openweather_API

Weather Reporting Dashboard
Project Overview
This project delivers a comprehensive, interactive weather reporting system that includes:

A Web-based weather dashboard (Web_page_weather_report.py)

A GUI-based desktop application (GuI_weather_report.py)

Both modules utilize the OpenWeatherMap API to fetch real-time and forecasted weather data and visualize it using intuitive, modern design standards. The goal is to provide rich weather insights to users through an engaging UI/UX experience.

Features
Web-based Weather Dashboard
Built-in interactive HTML weather dashboard generation

Visualizes:

Current weather summary

5-day temperature trends

Weather condition distribution (pie/bar)

Correlation heatmap of weather variables

Daily and hourly summaries

Multi-city comparisons

Exported as a standalone .html file (no server required)

Responsive design with customized styles

Embedded base64 images (no external dependencies)

GUI-based Weather Dashboard (Tkinter)
User-friendly desktop application with a tabbed interface

Features:

Real-time weather reporting

5-day weather forecasts with charts

Multi-city weather comparisons

City browser and selection (search, filter by continent/country)

Save and export weather data

Real-time charting using embedded Matplotlib in Tkinter

Threaded API calls for non-blocking GUI operations

Technologies & Libraries Used
Library---------- Purpose
requests--------- API calls to OpenWeatherMap
pandas----------- Data processing and transformation
matplotlib------- Data visualization
seaborn---------- Enhanced chart aesthetics
tkinter---------- GUI creation (Python standard library)
dotenv----------- Load environment variables (API key)
Pillow----------- (PIL) Image processing (Tkinter UI icons/images)
base64----------- Encode charts as HTML-embeddable images
threading-------- Asynchronous data fetching for responsive UI
json------------- Handling API responses
datetime--------- Timestamp conversion and formatting
io.BytesIO------- In-memory chart rendering
queue------------ Thread communication in Tkinter GUI
os--------------- File I/O, path handling
warnings--------- Suppress unnecessary warnings

Setup Instructions

1. Clone the Repository
   bash
   Copy
   Edit
   git clone https://github.com/your-username/weather-dashboard.git
   cd weather-dashboard
2. Create .env File
   Create a .env file in the root directory with your API key:

ini
Copy
Edit
OPENWEATHER_API_KEY=your_api_key_here 3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt 4. Run the Applications
Web Dashboard (Generates HTML)
bash
Copy
Edit
python Web_page_weather_report.py
Follow CLI prompts

Opens the generated .html file in browser

GUI Application
bash
Copy
Edit
python GuI_weather_report.py
Interactive interface for forecasts and comparisons

Design Philosophy
This project aims to combine data analytics, user-centric design, and real-world API integration into a complete weather intelligence system. Key pillars include:

Visual storytelling: Clear charts and summaries

Responsiveness: Fast, fluid UI with threading

Modularity: Separated logic for API, visualization, UI

Accessibility: Both web and desktop experiences

Project Structure
bash
Copy
Edit
├── GuI_weather_report.py # GUI desktop application
├── Web_page_weather_report.py # Web dashboard generator
├── .env # API credentials (user created)
├── requirements.txt # Python dependencies
└── README.md # Documentation
Notes
Make sure your system supports GUI applications (Tkinter) for running the GUI.

Internet connection is required to fetch real-time data.

The project is scalable to include more visualizations or API integrations (e.g., air quality, pollen index).

License
This project is developed for internship learning purposes. For usage or distribution, please consult with the project supervisor.
