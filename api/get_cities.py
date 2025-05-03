import requests
from requests.structures import CaseInsensitiveDict
from api.bounding_box import get_geoapify_bbox
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('GEOAPIFY_API_KEY')

def get_places(location_name, category="camping", limit=12, api_key=api_key):

    bbox = get_geoapify_bbox(location_name)
    
    if not bbox:
        return {"error": "Invalid location or bounding box not found."}
    
    api_url = f"https://api.geoapify.com/v2/places?categories={category}&filter=rect:{bbox}&limit={limit}&apiKey={api_key}"
    # print(api_url)
    
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}
