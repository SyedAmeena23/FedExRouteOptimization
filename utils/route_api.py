import requests

def get_route(source, destination):
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{source};{destination}?overview=false"
    response = requests.get(osrm_url)

    if response.status_code == 200:
        data = response.json()
        try:
            distance = data['routes'][0]['distance']  # Distance in meters
            duration = data['routes'][0]['duration']  # Duration in seconds
            return {'distance': distance, 'duration': duration}
        except (KeyError, IndexError):
            raise KeyError("The OSRM API response does not contain the required 'distance' or 'duration' keys.")
    else:
        raise Exception(f"Failed to fetch route data. Status code: {response.status_code}, Response: {response.text}")
