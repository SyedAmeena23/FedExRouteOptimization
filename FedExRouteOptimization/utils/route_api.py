import requests

def get_route_data(source, destination):
    url = f"http://router.project-osrm.org/route/v1/driving/{source};{destination}?overview=full"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        route_coords = [
            [coord[1], coord[0]] for coord in data['routes'][0]['geometry']['coordinates']
        ]
        distance = data['routes'][0]['distance'] / 1000  # Convert to km
        return {"coordinates": route_coords, "distance": distance}
    return {"error": "Failed to fetch route data"}
