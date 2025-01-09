from flask import Flask, request, render_template
import folium
from utils.traffic_api import get_traffic_data
from utils.weather_api import get_weather_data
from utils.route_api import get_route_data

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>FedEx Route Optimization</h1>
    <form action="/route" method="post">
        <label>Source (latitude,longitude):</label>
        <input type="text" name="source" placeholder="e.g., 12.9716,77.5946" required><br><br>
        <label>Destination (latitude,longitude):</label>
        <input type="text" name="destination" placeholder="e.g., 28.7041,77.1025" required><br><br>
        <label>Vehicle Mileage (km/l):</label>
        <input type="number" name="mileage" step="0.1" required><br><br>
        <button type="submit">Get Route</button>
    </form>
    '''

@app.route('/route', methods=['POST'])
def route():
    source = request.form['source']
    destination = request.form['destination']
    mileage = float(request.form['mileage'])

    # Fetch route data using OSRM API
    route_data = get_route_data(source, destination)
    if "error" in route_data:
        return f"<h1>Error: {route_data['error']}</h1>"

    route_coords = route_data['coordinates']
    distance = route_data['distance']

    # Fetch traffic data using TomTom API
    traffic_data = get_traffic_data("your_tomtom_api_key", source)

    # Fetch weather data using AQICN API
    weather_data = get_weather_data("your_aqicn_api_key", "city_name")

    # Create a map with Folium
    route_map = folium.Map(location=route_coords[0], zoom_start=6)
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(route_map)
    folium.Marker(route_coords[0], tooltip="Source", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(route_coords[-1], tooltip="Destination", icon=folium.Icon(color="red")).add_to(route_map)

    # Save map to an HTML file
    map_file = 'templates/route_map.html'
    route_map.save(map_file)

    # Calculate emissions
    emissions = (distance / mileage) * 2.31  # Assuming 2.31 kg CO2 per liter of fuel

    return f'''
    <h1>Route Details</h1>
    <p>Source: {source}</p>
    <p>Destination: {destination}</p>
    <p>Distance: {distance:.2f} km</p>
    <p>Estimated CO2 Emissions: {emissions:.2f} kg</p>
    <a href="/route_map.html" target="_blank">View Route Map</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)
