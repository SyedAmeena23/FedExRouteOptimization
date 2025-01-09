from flask import Flask, render_template, request
from utils.route_api import get_route
from geopy.geocoders import Nominatim
import folium
import os

app = Flask(__name__)

# Function to calculate emissions (basic formula)
def calculate_emissions(distance, mileage):
    fuel_used = distance / (mileage * 1000)  # Distance is in meters
    emissions = fuel_used * 2.31  # 2.31 kg CO2 per liter of fuel
    return round(emissions, 2)

# Function to generate route map
def generate_route_map(source_coords, destination_coords):
    route_map = folium.Map(location=source_coords, zoom_start=6)
    folium.Marker(source_coords, tooltip="Source", icon=folium.Icon(color='green')).add_to(route_map)
    folium.Marker(destination_coords, tooltip="Destination", icon=folium.Icon(color='red')).add_to(route_map)
    folium.PolyLine([source_coords, destination_coords], color='blue', weight=2.5, opacity=1).add_to(route_map)
    route_map.save('templates/route_map.html')  # Save map to templates folder

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    try:
        source = request.form.get('source')
        destination = request.form.get('destination')
        mileage = float(request.form.get('mileage'))

        # Get coordinates
        geolocator = Nominatim(user_agent="fedex_optimization")
        source_location = geolocator.geocode(source)
        destination_location = geolocator.geocode(destination)

        if not source_location or not destination_location:
            return "Unable to get coordinates for the provided locations. Please try again."

        source_coords = (source_location.latitude, source_location.longitude)
        destination_coords = (destination_location.latitude, destination_location.longitude)

        # Get route data
        route_data = get_route(f"{source_coords[1]},{source_coords[0]}", f"{destination_coords[1]},{destination_coords[0]}")
        distance = route_data.get('distance', 0)  # In meters
        duration = route_data.get('duration', 0)  # In seconds

        # Calculate emissions
        emissions = calculate_emissions(distance, mileage)

        # Generate route map
        generate_route_map(source_coords, destination_coords)

        # Render template with data
        return render_template('route_map.html', 
                               emissions=emissions, 
                               distance=distance / 1000,  # Convert meters to kilometers
                               duration=duration / 60)   # Convert seconds to minutes
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
