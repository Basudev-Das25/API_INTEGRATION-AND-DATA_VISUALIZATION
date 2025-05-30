#!/usr/bin/env python3
"""
Integrated Weather Dashboard with Enhanced UI/UX
Creates a single comprehensive dashboard with all visualizations
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

class IntegratedWeatherDashboard:
    def __init__(self, api_key: str):
        """
        Initialize Integrated Weather Dashboard with API key
        
        Args:
            api_key (str): OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
        
        # Set up matplotlib style for better visuals
        plt.style.use('default')
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        
        # Custom color scheme
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'success': '#C73E1D',
            'background': '#F5F5F5',
            'text': '#333333'
        }
        
    def get_current_weather(self, city: str) -> Dict:
        """Fetch current weather data for a city"""
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {city}: {e}")
            return {}
    
    def get_forecast_data(self, city: str) -> Dict:
        """Fetch 5-day weather forecast for a city"""
        url = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast for {city}: {e}")
            return {}
    
    def process_current_weather(self, data: Dict) -> Dict:
        """Process current weather API response"""
        if not data:
            return {}
            
        return {
            'city': data.get('name', 'Unknown'),
            'country': data.get('sys', {}).get('country', 'Unknown'),
            'temperature': data.get('main', {}).get('temp', 0),
            'feels_like': data.get('main', {}).get('feels_like', 0),
            'humidity': data.get('main', {}).get('humidity', 0),
            'pressure': data.get('main', {}).get('pressure', 0),
            'wind_speed': data.get('wind', {}).get('speed', 0),
            'weather_condition': data.get('weather', [{}])[0].get('main', 'Unknown'),
            'description': data.get('weather', [{}])[0].get('description', 'Unknown'),
            'timestamp': datetime.now()
        }
    
    def process_forecast_data(self, data: Dict) -> pd.DataFrame:
        """Process forecast API response into DataFrame"""
        if not data or 'list' not in data:
            return pd.DataFrame()
        
        forecast_list = []
        city_name = data.get('city', {}).get('name', 'Unknown')
        
        for item in data['list']:
            forecast_list.append({
                'city': city_name,
                'datetime': pd.to_datetime(item['dt_txt']),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item.get('wind', {}).get('speed', 0),
                'weather_condition': item['weather'][0]['main'],
                'description': item['weather'][0]['description']
            })
        
        return pd.DataFrame(forecast_list)
    
    def plot_to_base64(self, fig):
        """Convert matplotlib figure to base64 string for HTML embedding"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)
        return image_base64
    
    def create_integrated_dashboard(self, city: str, multi_cities: List[str] = None) -> str:
        """
        Create integrated dashboard with all visualizations
        
        Args:
            city (str): Main city for detailed analysis
            multi_cities (List[str]): Cities for comparison
            
        Returns:
            str: HTML content for the dashboard
        """
        print(f"Creating integrated dashboard for {city}...")
        
        # Get current weather
        current_data = self.get_current_weather(city)
        current_weather = self.process_current_weather(current_data)
        
        # Get forecast data
        forecast_data = self.get_forecast_data(city)
        df = self.process_forecast_data(forecast_data)
        
        if df.empty:
            return "<h1>Unable to fetch weather data</h1>"
        
        # Create all visualizations
        chart_images = {}
        
        # 1. Current Weather Summary Card (text-based)
        current_summary = self.create_current_weather_html(current_weather)
        
        # 2. Temperature Trend Chart
        chart_images['temp_trend'] = self.create_temperature_trend_chart(df, city)
        
        # 3. Weather Conditions Distribution
        chart_images['conditions'] = self.create_conditions_chart(df, city)
        
        # 4. Correlation Heatmap
        chart_images['correlation'] = self.create_correlation_chart(df, city)
        
        # 5. Daily Summary
        chart_images['daily_summary'] = self.create_daily_summary_chart(df, city)
        
        # 6. Multi-city comparison if provided
        if multi_cities:
            chart_images['multi_city'] = self.create_multi_city_chart(multi_cities)
        
        # 7. Hourly breakdown
        chart_images['hourly'] = self.create_hourly_chart(df, city)
        
        # Generate HTML dashboard
        html_content = self.generate_html_dashboard(city, current_summary, chart_images)
        
        return html_content
    
    def create_current_weather_html(self, weather_data: Dict) -> str:
        """Create HTML for current weather summary"""
        if not weather_data:
            return "<p>No current weather data available</p>"
        
        return f"""
        <div class="current-weather-card">
            <div class="weather-header">
                <h2>{weather_data['city']}, {weather_data['country']}</h2>
                <p class="timestamp">Last updated: {weather_data['timestamp'].strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            <div class="weather-main">
                <div class="temperature">
                    <span class="temp-value">{weather_data['temperature']:.1f}°C</span>
                    <span class="feels-like">Feels like {weather_data['feels_like']:.1f}°C</span>
                </div>
                <div class="condition">
                    <h3>{weather_data['weather_condition']}</h3>
                    <p>{weather_data['description'].title()}</p>
                </div>
            </div>
            <div class="weather-details">
                <div class="detail-item">
                    <span class="label">Humidity</span>
                    <span class="value">{weather_data['humidity']}%</span>
                </div>
                <div class="detail-item">
                    <span class="label">Pressure</span>
                    <span class="value">{weather_data['pressure']} hPa</span>
                </div>
                <div class="detail-item">
                    <span class="label">Wind Speed</span>
                    <span class="value">{weather_data['wind_speed']} m/s</span>
                </div>
            </div>
        </div>
        """
    
    def create_temperature_trend_chart(self, df: pd.DataFrame, city: str) -> str:
        """Create temperature trend chart and return as base64"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(df['datetime'], df['temperature'], 
               marker='o', linewidth=3, markersize=6, 
               color=self.colors['primary'], label='Temperature')
        ax.plot(df['datetime'], df['feels_like'], 
               marker='s', linewidth=2, markersize=4, 
               color=self.colors['secondary'], label='Feels Like', alpha=0.8)
        
        ax.fill_between(df['datetime'], df['temperature'], alpha=0.3, 
                       color=self.colors['primary'])
        
        ax.set_title(f'5-Day Temperature Forecast - {city}', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date & Time', fontsize=12)
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        
        return self.plot_to_base64(fig)
    
    def create_conditions_chart(self, df: pd.DataFrame, city: str) -> str:
        """Create weather conditions chart and return as base64"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        condition_counts = df['weather_condition'].value_counts()
        colors = sns.color_palette("husl", len(condition_counts))
        
        wedges, texts, autotexts = ax1.pie(condition_counts.values, 
                                          labels=condition_counts.index,
                                          autopct='%1.1f%%', startangle=90, 
                                          colors=colors)
        ax1.set_title('Weather Conditions Distribution', fontsize=14, fontweight='bold')
        
        # Bar chart for better readability
        ax2.bar(condition_counts.index, condition_counts.values, 
               color=colors, alpha=0.8)
        ax2.set_title('Weather Conditions Frequency', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Occurrences')
        ax2.tick_params(axis='x', rotation=45)
        
        fig.suptitle(f'Weather Patterns - {city}', fontsize=16, fontweight='bold')
        fig.tight_layout()
        
        return self.plot_to_base64(fig)
    
    def create_correlation_chart(self, df: pd.DataFrame, city: str) -> str:
        """Create correlation heatmap and return as base64"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        numeric_cols = ['temperature', 'feels_like', 'humidity', 'pressure', 'wind_speed']
        correlation_matrix = df[numeric_cols].corr()
        
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        sns.heatmap(correlation_matrix, mask=mask, annot=True, 
                   cmap='RdYlBu_r', center=0, square=True, 
                   linewidths=0.5, cbar_kws={"shrink": .8}, ax=ax)
        
        ax.set_title(f'Weather Variables Correlation - {city}', 
                    fontsize=16, fontweight='bold', pad=20)
        
        fig.tight_layout()
        return self.plot_to_base64(fig)
    
    def create_daily_summary_chart(self, df: pd.DataFrame, city: str) -> str:
        """Create daily summary chart and return as base64"""
        df['date'] = df['datetime'].dt.date
        daily_summary = df.groupby('date').agg({
            'temperature': ['min', 'max', 'mean'],
            'humidity': 'mean',
            'pressure': 'mean',
            'wind_speed': 'mean'
        }).round(2)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Daily Weather Summary - {city}', fontsize=16, fontweight='bold')
        
        # Temperature range
        axes[0, 0].plot(daily_summary.index, daily_summary[('temperature', 'min')], 
                       marker='o', label='Min Temp', color=self.colors['primary'], linewidth=2)
        axes[0, 0].plot(daily_summary.index, daily_summary[('temperature', 'max')], 
                       marker='o', label='Max Temp', color=self.colors['accent'], linewidth=2)
        axes[0, 0].fill_between(daily_summary.index, 
                               daily_summary[('temperature', 'min')],
                               daily_summary[('temperature', 'max')], 
                               alpha=0.3, color=self.colors['primary'])
        axes[0, 0].set_title('Daily Temperature Range', fontweight='bold')
        axes[0, 0].set_ylabel('Temperature (°C)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Humidity
        bars1 = axes[0, 1].bar(range(len(daily_summary)), daily_summary[('humidity', 'mean')], 
                              color=self.colors['secondary'], alpha=0.8)
        axes[0, 1].set_title('Average Daily Humidity', fontweight='bold')
        axes[0, 1].set_ylabel('Humidity (%)')
        axes[0, 1].set_xticks(range(len(daily_summary)))
        axes[0, 1].set_xticklabels([str(d) for d in daily_summary.index], rotation=45)
        
        # Pressure
        axes[1, 0].plot(daily_summary.index, daily_summary[('pressure', 'mean')], 
                       marker='s', color=self.colors['success'], linewidth=3, markersize=8)
        axes[1, 0].set_title('Average Daily Pressure', fontweight='bold')
        axes[1, 0].set_ylabel('Pressure (hPa)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Wind Speed
        bars2 = axes[1, 1].bar(range(len(daily_summary)), daily_summary[('wind_speed', 'mean')], 
                              color=self.colors['accent'], alpha=0.8)
        axes[1, 1].set_title('Average Daily Wind Speed', fontweight='bold')
        axes[1, 1].set_ylabel('Wind Speed (m/s)')
        axes[1, 1].set_xticks(range(len(daily_summary)))
        axes[1, 1].set_xticklabels([str(d) for d in daily_summary.index], rotation=45)
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def create_multi_city_chart(self, cities: List[str]) -> str:
        """Create multi-city comparison chart and return as base64"""
        current_data = []
        
        for city in cities:
            weather_data = self.get_current_weather(city)
            processed_data = self.process_current_weather(weather_data)
            if processed_data:
                current_data.append(processed_data)
        
        if not current_data:
            return ""
        
        df = pd.DataFrame(current_data)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Multi-City Weather Comparison', fontsize=16, fontweight='bold')
        
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['accent'], self.colors['success']]
        
        # Temperature
        bars1 = axes[0, 0].bar(df['city'], df['temperature'], 
                              color=colors[:len(df)], alpha=0.8)
        axes[0, 0].set_title('Temperature Comparison', fontweight='bold')
        axes[0, 0].set_ylabel('Temperature (°C)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}°C', ha='center', va='bottom')
        
        # Humidity
        bars2 = axes[0, 1].bar(df['city'], df['humidity'], 
                              color=colors[:len(df)], alpha=0.8)
        axes[0, 1].set_title('Humidity Comparison', fontweight='bold')
        axes[0, 1].set_ylabel('Humidity (%)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Pressure
        bars3 = axes[1, 0].bar(df['city'], df['pressure'], 
                              color=colors[:len(df)], alpha=0.8)
        axes[1, 0].set_title('Pressure Comparison', fontweight='bold')
        axes[1, 0].set_ylabel('Pressure (hPa)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Wind Speed
        bars4 = axes[1, 1].bar(df['city'], df['wind_speed'], 
                              color=colors[:len(df)], alpha=0.8)
        axes[1, 1].set_title('Wind Speed Comparison', fontweight='bold')
        axes[1, 1].set_ylabel('Wind Speed (m/s)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def create_hourly_chart(self, df: pd.DataFrame, city: str) -> str:
        """Create hourly breakdown chart and return as base64"""
        df['hour'] = df['datetime'].dt.hour
        hourly_avg = df.groupby('hour').agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'pressure': 'mean'
        }).round(2)
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle(f'Hourly Weather Patterns - {city}', fontsize=16, fontweight='bold')
        
        # Temperature by hour
        axes[0].plot(hourly_avg.index, hourly_avg['temperature'], 
                    marker='o', linewidth=3, markersize=8, color=self.colors['primary'])
        axes[0].fill_between(hourly_avg.index, hourly_avg['temperature'], 
                           alpha=0.3, color=self.colors['primary'])
        axes[0].set_title('Average Temperature by Hour', fontweight='bold')
        axes[0].set_xlabel('Hour of Day')
        axes[0].set_ylabel('Temperature (°C)')
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xticks(range(0, 24, 3))
        
        # Humidity by hour
        axes[1].bar(hourly_avg.index, hourly_avg['humidity'], 
                   color=self.colors['secondary'], alpha=0.8)
        axes[1].set_title('Average Humidity by Hour', fontweight='bold')
        axes[1].set_xlabel('Hour of Day')
        axes[1].set_ylabel('Humidity (%)')
        axes[1].set_xticks(range(0, 24, 3))
        
        # Pressure by hour
        axes[2].plot(hourly_avg.index, hourly_avg['pressure'], 
                    marker='s', linewidth=3, markersize=6, color=self.colors['success'])
        axes[2].set_title('Average Pressure by Hour', fontweight='bold')
        axes[2].set_xlabel('Hour of Day')
        axes[2].set_ylabel('Pressure (hPa)')
        axes[2].grid(True, alpha=0.3)
        axes[2].set_xticks(range(0, 24, 3))
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def generate_html_dashboard(self, city: str, current_summary: str, chart_images: Dict[str, str]) -> str:
        """Generate complete HTML dashboard"""
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weather Dashboard - {city}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .dashboard-container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                
                .dashboard-header {{
                    background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                
                .dashboard-header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                
                .dashboard-header p {{
                    font-size: 1.2em;
                    opacity: 0.9;
                }}
                
                .dashboard-content {{
                    padding: 30px;
                }}
                
                .current-weather-card {{
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    border-radius: 15px;
                    padding: 30px;
                    margin-bottom: 30px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                }}
                
                .weather-header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                
                .weather-header h2 {{
                    font-size: 2em;
                    color: #2E86AB;
                    margin-bottom: 5px;
                }}
                
                .timestamp {{
                    color: #666;
                    font-size: 0.9em;
                }}
                
                .weather-main {{
                    display: flex;
                    justify-content: space-around;
                    align-items: center;
                    margin-bottom: 20px;
                    flex-wrap: wrap;
                }}
                
                .temperature {{
                    text-align: center;
                }}
                
                .temp-value {{
                    font-size: 4em;
                    font-weight: bold;
                    color: #2E86AB;
                    display: block;
                }}
                
                .feels-like {{
                    font-size: 1.1em;
                    color: #666;
                }}
                
                .condition {{
                    text-align: center;
                }}
                
                .condition h3 {{
                    font-size: 1.8em;
                    color: #A23B72;
                    margin-bottom: 5px;
                }}
                
                .weather-details {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }}
                
                .detail-item {{
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                
                .detail-item .label {{
                    font-weight: bold;
                    color: #333;
                }}
                
                .detail-item .value {{
                    font-size: 1.2em;
                    color: #2E86AB;
                    font-weight: bold;
                }}
                
                .charts-grid {{
                    display: grid;
                    grid-template-columns: 1fr;
                    gap: 30px;
                    margin-top: 30px;
                }}
                
                .chart-container {{
                    background: white;
                    border-radius: 15px;
                    padding: 20px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    border: 1px solid #eee;
                }}
                
                .chart-container img {{
                    width: 100%;
                    height: auto;
                    border-radius: 10px;
                }}
                
                .chart-title {{
                    font-size: 1.3em;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 15px;
                    text-align: center;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #eee;
                }}
                
                .footer {{
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    border-top: 1px solid #eee;
                }}
                
                @media (max-width: 768px) {{
                    .weather-main {{
                        flex-direction: column;
                        gap: 20px;
                    }}
                    
                    .temp-value {{
                        font-size: 3em;
                    }}
                    
                    .dashboard-header h1 {{
                        font-size: 2em;
                    }}
                }}
                
                .loading {{
                    text-align: center;
                    padding: 50px;
                    color: #666;
                }}
                
                .error {{
                    background: #ffebee;
                    color: #c62828;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 4px solid #c62828;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard-container">
                <div class="dashboard-header">
                    <h1>🌤️ Weather Dashboard</h1>
                    <p>Comprehensive Weather Analysis & Forecast</p>
                </div>
                
                <div class="dashboard-content">
                    {current_summary}
                    
                    <div class="charts-grid">
                        {"".join([
                            f'''
                            <div class="chart-container">
                                <div class="chart-title">{title}</div>
                                <img src="data:image/png;base64,{image}" alt="{title}">
                            </div>
                            ''' for title, image in {
                                'Temperature Forecast': chart_images.get('temp_trend', ''),
                                'Weather Conditions Analysis': chart_images.get('conditions', ''),
                                'Weather Variables Correlation': chart_images.get('correlation', ''),
                                'Daily Weather Summary': chart_images.get('daily_summary', ''),
                                'Hourly Weather Patterns': chart_images.get('hourly', ''),
                                'Multi-City Comparison': chart_images.get('multi_city', '')
                            }.items() if image
                        ])}
                    </div>
                </div>
                
                <div class="footer">
                    <p>Data provided by OpenWeatherMap API | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Weather Dashboard v2.0 | Refresh for latest data</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def save_dashboard(self, city: str, multi_cities: List[str] = None, filename: str = None) -> str:
        """
        Generate and save integrated dashboard as HTML file
        
        Args:
            city (str): Main city for analysis
            multi_cities (List[str]): Cities for comparison
            filename (str): Output filename
            
        Returns:
            str: Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weather_dashboard_{city.replace(' ', '_')}_{timestamp}.html"
        
        html_content = self.create_integrated_dashboard(city, multi_cities)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard saved as: {filename}")
        print(f"📊 Open the file in your web browser to view the dashboard")

        return filename

def main():
    """
    Main function to demonstrate the Integrated Weather Dashboard
    """
    print("🌤️  Integrated Weather Dashboard")
    print("=" * 50)
    
    # Get API key from environment or user input
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        print("⚠️  OpenWeatherMap API key not found in environment variables.")
        print("Please set OPENWEATHER_API_KEY in your .env file or enter it below:")
        api_key = input("Enter your API key: ").strip()
        
        if not api_key:
            print("❌ API key is required. Exiting...")
            return
    
    # Initialize dashboard
    dashboard = IntegratedWeatherDashboard(api_key)
    
    # Get user input for cities
    print("\n📍 Enter the main city for detailed analysis:")
    main_city = input("Main city: ").strip()
    
    if not main_city:
        print("❌ Main city is required. Exiting...")
        return
    
    print(f"\n🌍 Enter additional cities for comparison (optional):")
    print("Enter cities separated by commas, or press Enter to skip:")
    multi_cities_input = input("Additional cities: ").strip()
    
    multi_cities = []
    if multi_cities_input:
        multi_cities = [city.strip() for city in multi_cities_input.split(',') if city.strip()]
        print(f"✅ Will compare with: {', '.join(multi_cities)}")
    
    try:
        # Generate and save dashboard
        print(f"\n🔄 Generating comprehensive dashboard for {main_city}...")
        filename = dashboard.save_dashboard(main_city, multi_cities)
        
        print(f"\n🎉 Success! Dashboard created successfully!")
        print(f"📄 File: {filename}")
        print(f"🌐 Open this file in your web browser to view the interactive dashboard")
        
        # Display some quick stats
        print(f"\n📊 Dashboard includes:")
        print("   • Current weather conditions")
        print("   • 5-day temperature forecast")
        print("   • Weather patterns analysis")
        print("   • Correlation heatmaps")
        print("   • Daily and hourly breakdowns")
        if multi_cities:
            print("   • Multi-city comparisons")
        
    except Exception as e:
        print(f"❌ Error creating dashboard: {e}")
        print("Please check your API key and internet connection.")

def demo_cities():
    """
    Demo function with predefined cities for quick testing
    """
    print("🚀 Running demo with predefined cities...")
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("❌ Please set OPENWEATHER_API_KEY environment variable for demo")
        return
    
    dashboard = IntegratedWeatherDashboard(api_key)
    
    # Demo cities
    main_city = "London"
    comparison_cities = ["New York", "Tokyo", "Sydney"]
    
    print(f"🎯 Main city: {main_city}")
    print(f"🌍 Comparison cities: {', '.join(comparison_cities)}")
    
    try:
        filename = dashboard.save_dashboard(main_city, comparison_cities)
        print(f"✅ Demo dashboard created: {filename}")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

class WeatherAnalytics:
    """
    Additional analytics utilities for weather data
    """
    
    @staticmethod
    def calculate_weather_score(temperature: float, humidity: float, wind_speed: float) -> float:
        """
        Calculate a simple weather comfort score (0-100)
        
        Args:
            temperature (float): Temperature in Celsius
            humidity (float): Humidity percentage
            wind_speed (float): Wind speed in m/s
            
        Returns:
            float: Weather comfort score
        """
        # Ideal conditions: 20-25°C, 40-60% humidity, 0-5 m/s wind
        temp_score = max(0, 100 - abs(temperature - 22.5) * 4)
        humidity_score = max(0, 100 - abs(humidity - 50) * 2)
        wind_score = max(0, 100 - max(0, wind_speed - 5) * 10)
        
        return (temp_score + humidity_score + wind_score) / 3
    
    @staticmethod
    def predict_rain_probability(humidity: float, pressure: float) -> str:
        """
        Simple rain prediction based on humidity and pressure
        
        Args:
            humidity (float): Humidity percentage
            pressure (float): Atmospheric pressure in hPa
            
        Returns:
            str: Rain probability description
        """
        if humidity > 80 and pressure < 1013:
            return "High"
        elif humidity > 60 and pressure < 1015:
            return "Medium"
        elif humidity > 40:
            return "Low"
        else:
            return "Very Low"
    
    @staticmethod
    def get_clothing_recommendation(temperature: float, wind_speed: float, condition: str) -> str:
        """
        Get clothing recommendations based on weather
        
        Args:
            temperature (float): Temperature in Celsius
            wind_speed (float): Wind speed in m/s
            condition (str): Weather condition
            
        Returns:
            str: Clothing recommendation
        """
        # Calculate feels-like temperature with wind chill
        feels_like = temperature - (wind_speed * 2)
        
        if feels_like < 0:
            return "Heavy winter coat, gloves, hat, and warm boots"
        elif feels_like < 10:
            return "Warm jacket, long pants, and closed shoes"
        elif feels_like < 20:
            return "Light jacket or sweater, long pants"
        elif feels_like < 25:
            return "T-shirt or light shirt, comfortable pants"
        else:
            return "Light clothing, shorts, and sandals"

def create_config_file():
    """
    Create a sample configuration file for the dashboard
    """
    config = {
        "default_cities": ["London", "New York", "Tokyo", "Sydney"],
        "api_settings": {
            "timeout": 30,
            "units": "metric",
            "retries": 3
        },
        "dashboard_settings": {
            "theme": "modern",
            "chart_colors": ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D"],
            "auto_refresh": False,
            "include_analytics": True
        },
        "output_settings": {
            "save_data": True,
            "export_csv": False,
            "include_timestamp": True
        }
    }
    
    with open('weather_config.json', 'w') as f:
        json.dump(config, indent=4, fp=f)
    
    print("✅ Configuration file created: weather_config.json")

def load_config():
    """
    Load configuration from file
    
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open('weather_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  Configuration file not found, using defaults")
        return {}

# Import numpy for correlation calculations
import numpy as np

if __name__ == "__main__":
    print("🌤️  Integrated Weather Dashboard System")
    print("=" * 60)
    print("Choose an option:")
    print("1. Create custom dashboard")
    print("2. Run demo with sample cities")
    print("3. Create configuration file")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        demo_cities()
    elif choice == "3":
        create_config_file()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Running main function...")
        main()