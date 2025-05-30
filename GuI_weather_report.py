#!/usr/bin/env python3
"""
Enhanced Weather Dashboard GUI Application
A comprehensive weather application with modern GUI interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
import threading
import queue
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

class WorldCitiesDatabase:
    """Database of major world cities organized by continent and country"""
    
    def __init__(self):
        self.cities = {
            "North America": {
                "United States": [
                    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
                    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
                    "Austin", "Jacksonville", "San Francisco", "Columbus", "Charlotte",
                    "Fort Worth", "Indianapolis", "Seattle", "Denver", "Washington DC",
                    "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City",
                    "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore",
                    "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
                    "Kansas City", "Mesa", "Atlanta", "Colorado Springs", "Omaha",
                    "Raleigh", "Miami", "Cleveland", "Tulsa", "Oakland", "Minneapolis"
                ],
                "Canada": [
                    "Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton",
                    "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Kitchener",
                    "London", "Victoria", "Halifax", "Oshawa", "Windsor"
                ],
                "Mexico": [
                    "Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana",
                    "León", "Juárez", "Torreón", "Querétaro", "San Luis Potosí"
                ]
            },
            "South America": {
                "Brazil": [
                    "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza",
                    "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"
                ],
                "Argentina": [
                    "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Tucumán",
                    "La Plata", "Mar del Plata", "Salta", "Santa Fe", "San Juan"
                ],
                "Chile": [
                    "Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta",
                    "Temuco", "Rancagua", "Talca", "Arica", "Chillán"
                ],
                "Colombia": [
                    "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
                    "Cúcuta", "Bucaramanga", "Pereira", "Santa Marta", "Ibagué"
                ]
            },
            "Europe": {
                "United Kingdom": [
                    "London", "Birmingham", "Manchester", "Glasgow", "Liverpool",
                    "Leeds", "Sheffield", "Edinburgh", "Bristol", "Cardiff"
                ],
                "Germany": [
                    "Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt",
                    "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig"
                ],
                "France": [
                    "Paris", "Marseille", "Lyon", "Toulouse", "Nice",
                    "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"
                ],
                "Italy": [
                    "Rome", "Milan", "Naples", "Turin", "Palermo",
                    "Genoa", "Bologna", "Florence", "Bari", "Catania"
                ],
                "Spain": [
                    "Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza",
                    "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao"
                ],
                "Russia": [
                    "Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Nizhny Novgorod",
                    "Kazan", "Chelyabinsk", "Omsk", "Samara", "Rostov-on-Don"
                ]
            },
            "Asia": {
                "China": [
                    "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Tianjin",
                    "Wuhan", "Dongguan", "Chengdu", "Nanjing", "Chongqing"
                ],
                "India": [
                    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad",
                    "Chennai", "Kolkata", "Surat", "Pune", "Jaipur"
                ],
                "Japan": [
                    "Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo",
                    "Fukuoka", "Kobe", "Kawasaki", "Kyoto", "Saitama"
                ],
                "South Korea": [
                    "Seoul", "Busan", "Incheon", "Daegu", "Daejeon",
                    "Gwangju", "Suwon", "Ulsan", "Changwon", "Goyang"
                ],
                "Thailand": [
                    "Bangkok", "Samut Prakan", "Mueang Nonthaburi", "Udon Thani", "Chon Buri",
                    "Nakhon Ratchasima", "Chiang Mai", "Hat Yai", "Pak Kret", "Si Racha"
                ]
            },
            "Africa": {
                "Nigeria": [
                    "Lagos", "Kano", "Ibadan", "Kaduna", "Port Harcourt",
                    "Benin City", "Maiduguri", "Zaria", "Aba", "Jos"
                ],
                "Egypt": [
                    "Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said",
                    "Suez", "Luxor", "Mansoura", "El Mahalla El Kubra", "Tanta"
                ],
                "South Africa": [
                    "Cape Town", "Johannesburg", "Durban", "Pretoria", "Port Elizabeth",
                    "Pietermaritzburg", "Benoni", "Tembisa", "East London", "Vereeniging"
                ]
            },
            "Oceania": {
                "Australia": [
                    "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
                    "Gold Coast", "Newcastle", "Canberra", "Sunshine Coast", "Wollongong"
                ],
                "New Zealand": [
                    "Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga",
                    "Napier-Hastings", "Dunedin", "Palmerston North", "Nelson", "Rotorua"
                ]
            }
        }
    
    def get_all_cities(self) -> List[str]:
        """Get a flat list of all cities"""
        all_cities = []
        for continent in self.cities.values():
            for country in continent.values():
                all_cities.extend(country)
        return sorted(all_cities)
    
    def get_cities_by_continent(self, continent: str) -> List[str]:
        """Get all cities in a specific continent"""
        if continent not in self.cities:
            return []
        cities = []
        for country in self.cities[continent].values():
            cities.extend(country)
        return sorted(cities)
    
    def get_cities_by_country(self, country: str) -> List[str]:
        """Get all cities in a specific country"""
        for continent in self.cities.values():
            if country in continent:
                return sorted(continent[country])
        return []
    
    def search_cities(self, query: str) -> List[str]:
        """Search cities by partial name match"""
        query = query.lower()
        matching_cities = []
        for continent in self.cities.values():
            for country in continent.values():
                for city in country:
                    if query in city.lower():
                        matching_cities.append(city)
        return sorted(matching_cities)
    
    def get_popular_cities(self, limit: int = 50) -> List[str]:
        """Get most popular world cities"""
        popular = [
            "New York", "London", "Tokyo", "Paris", "Singapore", "Sydney", "Dubai",
            "Hong Kong", "Los Angeles", "Barcelona", "Amsterdam", "Seoul", "Berlin",
            "Rome", "Madrid", "Mumbai", "Bangkok", "Istanbul", "Vienna", "Prague",
            "Buenos Aires", "São Paulo", "Mexico City", "Cairo", "Moscow", "Delhi",
            "Shanghai", "Beijing", "Toronto", "Vancouver", "Montreal", "Chicago",
            "San Francisco", "Miami", "Las Vegas", "Orlando", "Boston", "Washington DC"
        ]
        return popular[:limit]

class WeatherAPI:
    """Weather API handler"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
    
    def get_weather_data(self, city: str) -> Optional[Dict]:
        """Fetch current weather data for a city"""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = self.session.get(f"{self.base_url}/weather", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None
    
    def get_forecast_data(self, city: str, days: int = 5) -> Optional[Dict]:
        """Fetch weather forecast data for a city"""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8
            }
            response = self.session.get(f"{self.base_url}/forecast", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

class CitySelectionDialog:
    """Dialog for selecting cities"""
    
    def __init__(self, parent, cities_db: WorldCitiesDatabase):
        self.parent = parent
        self.cities_db = cities_db
        self.selected_city = None
        self.dialog = None
        
    def show(self) -> Optional[str]:
        """Show city selection dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Select City")
        self.dialog.geometry("600x500")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        self.create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
        return self.selected_city
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search frame
        search_frame = ttk.LabelFrame(main_frame, text="Search Cities", padding=10)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 11))
        search_entry.pack(fill=tk.X, pady=(0, 5))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Selection method frame
        method_frame = ttk.LabelFrame(main_frame, text="Browse Cities", padding=10)
        method_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons for different selection methods
        btn_frame = ttk.Frame(method_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Popular Cities", 
                  command=self.show_popular_cities).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="By Continent", 
                  command=self.show_continents).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="All Cities", 
                  command=self.show_all_cities).pack(side=tk.LEFT)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Cities", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview for cities list
        self.tree = ttk.Treeview(results_frame, columns=('City',), show='tree headings', height=15)
        self.tree.heading('#0', text='#')
        self.tree.heading('City', text='City')
        self.tree.column('#0', width=50)
        self.tree.column('City', width=400)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', self.on_city_select)
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Select", command=self.on_city_select).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=self.on_cancel).pack(side=tk.RIGHT)
        
        # Show popular cities by default
        self.show_popular_cities()
    
    def populate_tree(self, cities: List[str], title: str = "Cities"):
        """Populate the tree with cities"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add cities
        for i, city in enumerate(cities, 1):
            self.tree.insert('', 'end', text=str(i), values=(city,))
    
    def on_search(self, event=None):
        """Handle search input"""
        query = self.search_var.get().strip()
        if len(query) >= 2:
            matches = self.cities_db.search_cities(query)
            self.populate_tree(matches, f"Search Results ({len(matches)} found)")
        elif len(query) == 0:
            self.show_popular_cities()
    
    def show_popular_cities(self):
        """Show popular cities"""
        popular = self.cities_db.get_popular_cities()
        self.populate_tree(popular, "Popular Cities")
    
    def show_continents(self):
        """Show continent selection"""
        continent_dialog = tk.Toplevel(self.dialog)
        continent_dialog.title("Select Continent")
        continent_dialog.geometry("300x400")
        continent_dialog.transient(self.dialog)
        continent_dialog.grab_set()
        
        frame = ttk.Frame(continent_dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Select a Continent:", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        for continent in self.cities_db.cities.keys():
            city_count = len(self.cities_db.get_cities_by_continent(continent))
            btn = ttk.Button(frame, text=f"{continent} ({city_count} cities)",
                           command=lambda c=continent: self.select_continent(c, continent_dialog))
            btn.pack(fill=tk.X, pady=2)
    
    def select_continent(self, continent: str, dialog: tk.Toplevel):
        """Handle continent selection"""
        cities = self.cities_db.get_cities_by_continent(continent)
        self.populate_tree(cities, f"{continent} Cities")
        dialog.destroy()
    
    def show_all_cities(self):
        """Show all cities"""
        all_cities = self.cities_db.get_all_cities()
        self.populate_tree(all_cities, f"All Cities ({len(all_cities)} total)")
    
    def on_city_select(self, event=None):
        """Handle city selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_city = item['values'][0]
            self.dialog.destroy()
    
    def on_cancel(self):
        """Handle cancel"""
        self.selected_city = None
        self.dialog.destroy()

class WeatherDashboardGUI:
    """Main GUI application for weather dashboard"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Weather Dashboard")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.cities_db = WorldCitiesDatabase()
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        
        if not self.api_key:
            messagebox.showerror("Error", 
                               "OpenWeatherMap API key not found!\n"
                               "Please set OPENWEATHER_API_KEY in your .env file")
            self.root.destroy()
            return
        
        self.weather_api = WeatherAPI(self.api_key)
        
        # Style configuration
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Current weather data storage
        self.current_weather_data = {}
        self.comparison_data = []
        
        # Queue for thread communication
        self.queue = queue.Queue()
        
        # Start queue processing
        self.process_queue()
    
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'accent': '#F18F01',
            'success': '#28A745',
            'warning': '#FFC107',
            'danger': '#DC3545',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
        
        # Set matplotlib style
        plt.style.use('default')
        sns.set_style("whitegrid")
    
    def create_widgets(self):
        """Create main application widgets"""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_current_weather_tab()
        self.create_forecast_tab()
        self.create_comparison_tab()
        self.create_cities_browser_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_current_weather_tab(self):
        """Create current weather tab"""
        # Current Weather Tab
        self.current_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.current_frame, text="Current Weather")
        
        # Top frame for controls
        top_frame = ttk.Frame(self.current_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Current Weather", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # City selection frame
        city_frame = ttk.LabelFrame(self.current_frame, text="City Selection", padding=10)
        city_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # City input with autocomplete
        input_frame = ttk.Frame(city_frame)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Enter City:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.city_var = tk.StringVar()
        self.city_entry = ttk.Entry(input_frame, textvariable=self.city_var, font=('Arial', 11))
        self.city_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(input_frame, text="Browse Cities", 
                  command=self.browse_cities_current).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(input_frame, text="Get Weather", 
                  command=self.get_current_weather).pack(side=tk.LEFT)
        
        # Weather display frame
        self.weather_display_frame = ttk.LabelFrame(self.current_frame, text="Weather Information", padding=10)
        self.weather_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrolled text for weather info
        self.weather_text = scrolledtext.ScrolledText(self.weather_display_frame, 
                                                     height=20, font=('Courier', 10))
        self.weather_text.pack(fill=tk.BOTH, expand=True)

        # Weather chart frame
        chart_frame = ttk.LabelFrame(self.weather_display_frame, text="Weather Chart", padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create matplotlib figure for current weather
        self.current_weather_fig = Figure(figsize=(8, 4), dpi=100)
        self.current_weather_canvas = FigureCanvasTkAgg(self.current_weather_fig, chart_frame)
        self.current_weather_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Buttons frame
        btn_frame = ttk.Frame(self.current_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Save Data", 
                  command=self.save_current_weather).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Clear", 
                  command=self.clear_current_weather).pack(side=tk.LEFT, padx=(5, 0))
    
    def create_forecast_tab(self):
        """Create forecast tab"""
        self.forecast_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.forecast_frame, text="Weather Forecast")
        
        # Top frame
        top_frame = ttk.Frame(self.forecast_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="5-Day Weather Forecast", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # City selection
        city_frame = ttk.LabelFrame(self.forecast_frame, text="City Selection", padding=10)
        city_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        input_frame = ttk.Frame(city_frame)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Enter City:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.forecast_city_var = tk.StringVar()
        self.forecast_city_entry = ttk.Entry(input_frame, textvariable=self.forecast_city_var, font=('Arial', 11))
        self.forecast_city_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(input_frame, text="Browse Cities", 
                  command=self.browse_cities_forecast).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(input_frame, text="Get Forecast", 
                  command=self.get_weather_forecast).pack(side=tk.LEFT)
        
        # Create paned window for forecast display and chart
        paned = ttk.PanedWindow(self.forecast_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Forecast text frame
        text_frame = ttk.LabelFrame(paned, text="Forecast Details", padding=10)
        paned.add(text_frame, weight=1)
        
        self.forecast_text = scrolledtext.ScrolledText(text_frame, height=25, font=('Courier', 10))
        self.forecast_text.pack(fill=tk.BOTH, expand=True)
        
        # Chart frame
        chart_frame = ttk.LabelFrame(paned, text="Forecast Chart", padding=10)
        paned.add(chart_frame, weight=2)
        
        # Create matplotlib figure
        self.forecast_fig = Figure(figsize=(8, 6), dpi=100)
        self.forecast_canvas = FigureCanvasTkAgg(self.forecast_fig, chart_frame)
        self.forecast_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_comparison_tab(self):
        """Create weather comparison tab"""
        self.comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.comparison_frame, text="City Comparison")
        
        # Top frame
        top_frame = ttk.Frame(self.comparison_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Weather Comparison", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # Cities selection frame
        cities_frame = ttk.LabelFrame(self.comparison_frame, text="Cities to Compare", padding=10)
        cities_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Cities listbox with scrollbar
        list_frame = ttk.Frame(cities_frame)
        list_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.cities_listbox = tk.Listbox(list_frame, height=4, font=('Arial', 10))
        list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.cities_listbox.config(yscrollcommand=list_scrollbar.set)
        list_scrollbar.config(command=self.cities_listbox.yview)
        
        self.cities_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons for city management
        btn_frame = ttk.Frame(cities_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add City", 
                  command=self.add_comparison_city).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Remove Selected", 
                  command=self.remove_comparison_city).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Clear All", 
                  command=self.clear_comparison_cities).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Compare Weather", 
                  command=self.compare_weather).pack(side=tk.RIGHT)
        
        # Results display
        results_paned = ttk.PanedWindow(self.comparison_frame, orient=tk.VERTICAL)
        results_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Comparison table
        table_frame = ttk.LabelFrame(results_paned, text="Comparison Table", padding=10)
        results_paned.add(table_frame, weight=1)
        
        # Treeview for comparison results
        columns = ('City', 'Temperature', 'Humidity', 'Pressure', 'Condition')
        self.comparison_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.comparison_tree.heading(col, text=col)
            self.comparison_tree.column(col, width=120)
        
        tree_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.comparison_tree.yview)
        self.comparison_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.comparison_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Comparison chart
        comp_chart_frame = ttk.LabelFrame(results_paned, text="Comparison Charts", padding=10)
        results_paned.add(comp_chart_frame, weight=2)
        
        self.comparison_fig = Figure(figsize=(10, 6), dpi=100)
        self.comparison_canvas = FigureCanvasTkAgg(self.comparison_fig, comp_chart_frame)
        self.comparison_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_cities_browser_tab(self):
        """Create cities browser tab"""
        self.browser_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.browser_frame, text="Cities Browser")
        
        # Top frame
        top_frame = ttk.Frame(self.browser_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Cities Browser", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # Search and filter frame
        search_frame = ttk.LabelFrame(self.browser_frame, text="Search & Filter", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Search row
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_row, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.browser_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_row, textvariable=self.browser_search_var, font=('Arial', 11))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self.on_browser_search)
        
        # Filter row
        filter_row = ttk.Frame(search_frame)
        filter_row.pack(fill=tk.X)
        
        ttk.Label(filter_row, text="Filter by:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="All Cities")
        filter_combo = ttk.Combobox(filter_row, textvariable=self.filter_var, 
                                   values=["All Cities", "Popular Cities"] + list(self.cities_db.cities.keys()),
                                   state="readonly", width=20)
        filter_combo.pack(side=tk.LEFT, padx=(0, 5))
        filter_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        ttk.Button(filter_row, text="Refresh", command=self.refresh_cities_browser).pack(side=tk.LEFT)
        
        # Cities display
        display_frame = ttk.LabelFrame(self.browser_frame, text="Cities", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Treeview for cities
        columns = ('City', 'Continent', 'Country')
        self.browser_tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.browser_tree.heading(col, text=col)
            self.browser_tree.column(col, width=150)
        
        browser_scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.browser_tree.yview)
        self.browser_tree.configure(yscrollcommand=browser_scrollbar.set)
        
        self.browser_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        browser_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to get weather
        self.browser_tree.bind('<Double-1>', self.get_weather_from_browser)
        
        # Initialize with all cities
        self.refresh_cities_browser()
    
    def on_browser_search(self, event=None):
        """Handle search in cities browser"""
        query = self.browser_search_var.get().strip()
        if len(query) >= 2:
            matches = self.cities_db.search_cities(query)
            self.populate_browser_tree(matches)
        elif len(query) == 0:
            self.refresh_cities_browser()
    
    def on_filter_change(self, event=None):
        """Handle filter change in cities browser"""
        self.refresh_cities_browser()
    
    def refresh_cities_browser(self):
        """Refresh cities browser display"""
        filter_value = self.filter_var.get()
        
        if filter_value == "All Cities":
            cities = self.cities_db.get_all_cities()
        elif filter_value == "Popular Cities":
            cities = self.cities_db.get_popular_cities()
        elif filter_value in self.cities_db.cities:
            cities = self.cities_db.get_cities_by_continent(filter_value)
        else:
            cities = []
        
        self.populate_browser_tree(cities)
    
    def populate_browser_tree(self, cities):
        """Populate browser tree with cities"""
        # Clear existing items
        for item in self.browser_tree.get_children():
            self.browser_tree.delete(item)
        
        # Add cities with continent and country info
        for city in cities:
            continent, country = self.find_city_location(city)
            self.browser_tree.insert('', 'end', values=(city, continent, country))
    
    def find_city_location(self, city):
        """Find continent and country for a city"""
        for continent, countries in self.cities_db.cities.items():
            for country, cities in countries.items():
                if city in cities:
                    return continent, country
        return "Unknown", "Unknown"
    
    def get_weather_from_browser(self, event=None):
        """Get weather for selected city from browser"""
        selection = self.browser_tree.selection()
        if selection:
            item = self.browser_tree.item(selection[0])
            city = item['values'][0]
            
            # Switch to current weather tab and set city
            self.notebook.select(0)  # Select first tab (Current Weather)
            self.city_var.set(city)
            self.get_current_weather()
    
    def browse_cities_current(self):
        """Browse cities for current weather"""
        dialog = CitySelectionDialog(self.root, self.cities_db)
        selected_city = dialog.show()
        if selected_city:
            self.city_var.set(selected_city)
    
    def browse_cities_forecast(self):
        """Browse cities for forecast"""
        dialog = CitySelectionDialog(self.root, self.cities_db)
        selected_city = dialog.show()
        if selected_city:
            self.forecast_city_var.set(selected_city)
    
    def get_current_weather(self):
        """Get current weather data"""
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        self.status_var.set(f"Fetching weather data for {city}...")
        self.weather_text.delete(1.0, tk.END)
        self.weather_text.insert(tk.END, "Loading weather data...\n")
        
        # Start background thread for API call
        thread = threading.Thread(target=self.fetch_current_weather, args=(city,))
        thread.daemon = True
        thread.start()
    
    def fetch_current_weather(self, city):
        """Fetch current weather in background thread"""
        try:
            weather_data = self.weather_api.get_weather_data(city)
            self.queue.put(('current_weather', weather_data, city))
        except Exception as e:
            self.queue.put(('error', str(e), city))
    
    def get_weather_forecast(self):
        """Get weather forecast data"""
        city = self.forecast_city_var.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        self.status_var.set(f"Fetching forecast data for {city}...")
        self.forecast_text.delete(1.0, tk.END)
        self.forecast_text.insert(tk.END, "Loading forecast data...\n")
        
        # Clear previous chart
        self.forecast_fig.clear()
        self.forecast_canvas.draw()
        
        # Start background thread for API call
        thread = threading.Thread(target=self.fetch_forecast, args=(city,))
        thread.daemon = True
        thread.start()
    
    def fetch_forecast(self, city):
        """Fetch forecast in background thread"""
        try:
            forecast_data = self.weather_api.get_forecast_data(city)
            self.queue.put(('forecast', forecast_data, city))
        except Exception as e:
            self.queue.put(('error', str(e), city))
    
    def add_comparison_city(self):
        """Add city to comparison list"""
        dialog = CitySelectionDialog(self.root, self.cities_db)
        selected_city = dialog.show()
        if selected_city:
            # Check if city already in list
            current_cities = [self.cities_listbox.get(i) for i in range(self.cities_listbox.size())]
            if selected_city not in current_cities:
                self.cities_listbox.insert(tk.END, selected_city)
    
    def remove_comparison_city(self):
        """Remove selected city from comparison list"""
        selection = self.cities_listbox.curselection()
        if selection:
            self.cities_listbox.delete(selection[0])
    
    def clear_comparison_cities(self):
        """Clear all cities from comparison list"""
        self.cities_listbox.delete(0, tk.END)
        # Clear comparison results
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        self.comparison_fig.clear()
        self.comparison_canvas.draw()
    
    def compare_weather(self):
        """Compare weather for selected cities"""
        cities = [self.cities_listbox.get(i) for i in range(self.cities_listbox.size())]
        
        if len(cities) < 2:
            messagebox.showwarning("Warning", "Please add at least 2 cities for comparison")
            return
        
        self.status_var.set("Fetching weather data for comparison...")
        
        # Clear previous results
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        
        # Start background thread for comparison
        thread = threading.Thread(target=self.fetch_comparison_data, args=(cities,))
        thread.daemon = True
        thread.start()
    
    def fetch_comparison_data(self, cities):
        """Fetch comparison data in background thread"""
        comparison_results = []
        
        for city in cities:
            try:
                weather_data = self.weather_api.get_weather_data(city)
                if weather_data:
                    comparison_results.append({
                        'city': city,
                        'data': weather_data
                    })
            except Exception as e:
                print(f"Error fetching data for {city}: {e}")
        
        self.queue.put(('comparison', comparison_results, None))
    
    def display_current_weather(self, weather_data, city):
        """Display current weather data"""
        self.weather_text.delete(1.0, tk.END)
        
        if not weather_data:
            self.weather_text.insert(tk.END, f"Error: Could not fetch weather data for {city}\n")
            self.status_var.set("Error fetching weather data")
            return
        
        self.current_weather_data = weather_data
        
        # Format weather information
        weather_info = self.format_current_weather(weather_data)
        self.weather_text.insert(tk.END, weather_info)
        
        # Create current weather chart
        self.create_current_weather_chart(weather_data)
        
        self.status_var.set(f"Weather data loaded for {city}")
    
    def create_current_weather_chart(self, weather_data):
        """Create current weather visualization chart"""
        try:
            self.current_weather_fig.clear()
            
            # Extract data for plotting
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            
            # Create subplots
            ax1 = self.current_weather_fig.add_subplot(2, 2, 1)
            ax2 = self.current_weather_fig.add_subplot(2, 2, 2)
            ax3 = self.current_weather_fig.add_subplot(2, 2, 3)
            ax4 = self.current_weather_fig.add_subplot(2, 2, 4)
            
            # Temperature gauge
            ax1.pie([temp, 40-temp], colors=['#FF6B6B', '#E0E0E0'], startangle=90)
            ax1.text(0, 0, f'{temp}°C', ha='center', va='center', fontsize=12, fontweight='bold')
            ax1.set_title('Current Temperature', fontsize=10, fontweight='bold')
            
            # Feels like gauge
            ax2.pie([feels_like, 40-feels_like], colors=['#4ECDC4', '#E0E0E0'], startangle=90)
            ax2.text(0, 0, f'{feels_like}°C', ha='center', va='center', fontsize=12, fontweight='bold')
            ax2.set_title('Feels Like', fontsize=10, fontweight='bold')
            
            # Humidity gauge
            ax3.pie([humidity, 100-humidity], colors=['#45B7D1', '#E0E0E0'], startangle=90)
            ax3.text(0, 0, f'{humidity}%', ha='center', va='center', fontsize=12, fontweight='bold')
            ax3.set_title('Humidity', fontsize=10, fontweight='bold')
            
            # Pressure gauge
            normalized_pressure = (pressure - 900) / (1100 - 900) * 100  # Normalize to 0-100
            ax4.pie([normalized_pressure, 100-normalized_pressure], colors=['#96CEB4', '#E0E0E0'], startangle=90)
            ax4.text(0, 0, f'{pressure}\nhPa', ha='center', va='center', fontsize=10, fontweight='bold')
            ax4.set_title('Pressure', fontsize=10, fontweight='bold')
            
            self.current_weather_fig.tight_layout()
            self.current_weather_canvas.draw()
            
        except Exception as e:
            print(f"Error creating current weather chart: {e}")
    
    def format_current_weather(self, data):
        """Format current weather data for display"""
        try:
            city = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            description = data['weather'][0]['description'].title()
            wind_speed = data['wind']['speed']
            wind_deg = data['wind'].get('deg', 0)
            visibility = data.get('visibility', 'N/A')
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
            
            weather_info = f"""
╔══════════════════════════════════════════════════════════════╗
║                     CURRENT WEATHER REPORT                   ║
╠══════════════════════════════════════════════════════════════╣
║ Location: {city}, {country}
║ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
║
║ TEMPERATURE INFORMATION:
║ ├─ Current Temperature: {temp}°C
║ ├─ Feels Like: {feels_like}°C
║ ├─ Condition: {description}
║
║ ATMOSPHERIC CONDITIONS:
║ ├─ Humidity: {humidity}%
║ ├─ Pressure: {pressure} hPa
║ ├─ Visibility: {visibility/1000 if visibility != 'N/A' else 'N/A'} km
║
║ WIND INFORMATION:
║ ├─ Speed: {wind_speed} m/s
║ ├─ Direction: {wind_deg}°
║
║ SUN INFORMATION:
║ ├─ Sunrise: {sunrise}
║ ├─ Sunset: {sunset}
║
╚══════════════════════════════════════════════════════════════╝
            """
            
            return weather_info.strip()
            
        except KeyError as e:
            return f"Error formatting weather data: Missing key {e}"
    
    def display_forecast(self, forecast_data, city):
        """Display forecast data"""
        self.forecast_text.delete(1.0, tk.END)
        
        if not forecast_data:
            self.forecast_text.insert(tk.END, f"Error: Could not fetch forecast data for {city}\n")
            self.status_var.set("Error fetching forecast data")
            return
        
        # Format forecast information
        forecast_info = self.format_forecast(forecast_data)
        self.forecast_text.insert(tk.END, forecast_info)
        
        # Create forecast chart
        self.create_forecast_chart(forecast_data)
        
        self.status_var.set(f"Forecast data loaded for {city}")
    
    def format_forecast(self, data):
        """Format forecast data for display"""
        try:
            city = data['city']['name']
            country = data['city']['country']
            
            forecast_info = f"""
╔══════════════════════════════════════════════════════════════╗
║                    5-DAY WEATHER FORECAST                    ║
╠══════════════════════════════════════════════════════════════╣
║ Location: {city}, {country}
║ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
║
╚══════════════════════════════════════════════════════════════╝

"""
            
            # Group forecasts by day
            daily_forecasts = {}
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append(item)
            
            # Display daily summaries
            for date, forecasts in list(daily_forecasts.items())[:5]:  # Show 5 days
                date_str = date.strftime('%A, %B %d, %Y')
                forecast_info += f"\n{date_str}\n" + "="*60 + "\n"
                
                # Get daily min/max temperatures
                temps = [f['main']['temp'] for f in forecasts]
                min_temp = min(temps)
                max_temp = max(temps)
                
                # Get most common weather condition
                conditions = [f['weather'][0]['description'] for f in forecasts]
                most_common_condition = max(set(conditions), key=conditions.count).title()
                
                # Calculate average humidity and pressure
                avg_humidity = sum(f['main']['humidity'] for f in forecasts) / len(forecasts)
                avg_pressure = sum(f['main']['pressure'] for f in forecasts) / len(forecasts)
                
                forecast_info += f"""
Temperature Range: {min_temp:.1f}°C - {max_temp:.1f}°C
Condition: {most_common_condition}
Average Humidity: {avg_humidity:.0f}%
Average Pressure: {avg_pressure:.0f} hPa

Hourly Details:
"""
                for forecast in forecasts[:4]:  # Show first 4 hourly forecasts per day
                    time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
                    temp = forecast['main']['temp']
                    desc = forecast['weather'][0]['description'].title()
                    forecast_info += f"  {time}: {temp}°C, {desc}\n"
                
                forecast_info += "\n"
            
            return forecast_info
            
        except KeyError as e:
            return f"Error formatting forecast data: Missing key {e}"
    
    def create_forecast_chart(self, forecast_data):
        """Create forecast chart"""
        try:
            self.forecast_fig.clear()
            
            # Extract data for plotting
            timestamps = []
            temperatures = []
            humidity = []
            
            for item in forecast_data['list'][:20]:  # Show first 20 forecasts (about 2.5 days)
                timestamps.append(datetime.fromtimestamp(item['dt']))
                temperatures.append(item['main']['temp'])
                humidity.append(item['main']['humidity'])
            
            # Create subplots
            ax1 = self.forecast_fig.add_subplot(2, 1, 1)
            ax2 = self.forecast_fig.add_subplot(2, 1, 2)
            
            # Temperature plot
            ax1.plot(timestamps, temperatures, color='#FF6B6B', linewidth=2, marker='o', markersize=4)
            ax1.set_title('Temperature Forecast', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Temperature (°C)')
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
            
            # Humidity plot
            ax2.plot(timestamps, humidity, color='#4ECDC4', linewidth=2, marker='s', markersize=4)
            ax2.set_title('Humidity Forecast', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Humidity (%)')
            ax2.set_xlabel('Time')
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
            
            self.forecast_fig.tight_layout()
            self.forecast_canvas.draw()
            
        except Exception as e:
            print(f"Error creating forecast chart: {e}")
    
    def display_comparison(self, comparison_results):
        """Display weather comparison results"""
        if not comparison_results:
            messagebox.showwarning("Warning", "No weather data could be retrieved for comparison")
            return
        
        # Clear previous results
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        
        # Populate comparison table
        for result in comparison_results:
            city = result['city']
            data = result['data']
            
            temp = f"{data['main']['temp']:.1f}°C"
            humidity = f"{data['main']['humidity']}%"
            pressure = f"{data['main']['pressure']} hPa"
            condition = data['weather'][0]['description'].title()
            
            self.comparison_tree.insert('', 'end', values=(city, temp, humidity, pressure, condition))
        
        # Create comparison charts
        self.create_comparison_charts(comparison_results)
        
        self.status_var.set(f"Comparison complete for {len(comparison_results)} cities")
    
    def create_comparison_charts(self, comparison_results):
        """Create comparison charts"""
        try:
            self.comparison_fig.clear()
            
            cities = [result['city'] for result in comparison_results]
            temperatures = [result['data']['main']['temp'] for result in comparison_results]
            humidity = [result['data']['main']['humidity'] for result in comparison_results]
            pressure = [result['data']['main']['pressure'] for result in comparison_results]
            
            # Create subplots
            ax1 = self.comparison_fig.add_subplot(2, 2, 1)
            ax2 = self.comparison_fig.add_subplot(2, 2, 2)
            ax3 = self.comparison_fig.add_subplot(2, 2, 3)
            ax4 = self.comparison_fig.add_subplot(2, 2, 4)
            
            # Temperature bar chart
            bars1 = ax1.bar(cities, temperatures, color='#FF6B6B', alpha=0.7)
            ax1.set_title('Temperature Comparison', fontweight='bold')
            ax1.set_ylabel('Temperature (°C)')
            ax1.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, temp in zip(bars1, temperatures):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{temp:.1f}°C', ha='center', va='bottom', fontsize=8)
            
            # Humidity bar chart
            bars2 = ax2.bar(cities, humidity, color='#4ECDC4', alpha=0.7)
            ax2.set_title('Humidity Comparison', fontweight='bold')
            ax2.set_ylabel('Humidity (%)')
            ax2.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, hum in zip(bars2, humidity):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f'{hum}%', ha='center', va='bottom', fontsize=8)
            
            # Pressure bar chart
            bars3 = ax3.bar(cities, pressure, color='#45B7D1', alpha=0.7)
            ax3.set_title('Pressure Comparison', fontweight='bold')
            ax3.set_ylabel('Pressure (hPa)')
            ax3.tick_params(axis='x', rotation=45)
            
            # Temperature vs Humidity scatter plot
            ax4.scatter(temperatures, humidity, c=pressure, cmap='viridis', s=100, alpha=0.7)
            ax4.set_xlabel('Temperature (°C)')
            ax4.set_ylabel('Humidity (%)')
            ax4.set_title('Temperature vs Humidity', fontweight='bold')
            
            # Add city labels to scatter plot
            for i, city in enumerate(cities):
                ax4.annotate(city, (temperatures[i], humidity[i]), 
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
            
            self.comparison_fig.tight_layout()
            self.comparison_canvas.draw()
            
        except Exception as e:
            print(f"Error creating comparison charts: {e}")
    
    def save_current_weather(self):
        """Save current weather data to file"""
        if not self.current_weather_data:
            messagebox.showwarning("Warning", "No weather data to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(self.current_weather_data, f, indent=2)
                else:
                    weather_text = self.weather_text.get(1.0, tk.END)
                    with open(filename, 'w') as f:
                        f.write(weather_text)
                
                messagebox.showinfo("Success", f"Weather data saved to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def clear_current_weather(self):
        """Clear current weather display"""
        self.weather_text.delete(1.0, tk.END)
        self.current_weather_data = {}
        self.city_var.set("")
        self.status_var.set("Ready")
    
    def process_queue(self):
        """Process messages from background threads"""
        try:
            while True:
                message_type, data, city = self.queue.get_nowait()
                
                if message_type == 'current_weather':
                    self.display_current_weather(data, city)
                elif message_type == 'forecast':
                    self.display_forecast(data, city)
                elif message_type == 'comparison':
                    self.display_comparison(data)
                elif message_type == 'error':
                    messagebox.showerror("Error", f"Error fetching weather data for {city}: {data}")
                    self.status_var.set("Error occurred")
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_queue)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function to run the weather dashboard"""
    try:
        app = WeatherDashboardGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()