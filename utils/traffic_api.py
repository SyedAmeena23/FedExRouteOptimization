import requests

def get_traffic_data(api_key, location):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={location}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        traffic_info = {
            "current_speed": data['flowSegmentData']['currentSpeed'],
            "free_flow_speed": data['flowSegmentData']['freeFlowSpeed'],
            "congestion": data['flowSegmentData']['currentTravelTime']
        }
        return traffic_info
    return {"error": "Failed to fetch traffic data"}
