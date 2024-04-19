import os

import requests
from PIL import Image
from io import BytesIO
import creds
import json
import time

def fetch_and_open_image(url, headers):
    """Fetch an image from a URL and return it as an open PIL Image object."""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Failed to retrieve image from {url}. Status code: {response.status_code}")
        return None


def process_image_set(image_id, level, headers, schema, directory_path):
    """Process a set of images for both raw and lidar data."""
    sides = ['R', 'B', 'U', 'D', 'L', 'F']
    base_url = "https://atlascbs360yeni.ibb.gov.tr"

    for side in sides:
        for row, col in schema:
            url_raw = f"{base_url}/panoramatiles//Tile/{image_id}/{level}/{side}/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_23.4.0"

            image_raw = fetch_and_open_image(url_raw, headers)

        output_filename_raw = f"{directory_path}/{image_id}_raw_{side}.jpg"
        image_raw.save(output_filename_raw)

payload = {}
headers = {
    'Authorization': f'Basic {creds.api_key_2023}'
}


level = 2


if level == 1:
    schema = [
        (0, 0)
    ]


else:
    schema = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2)
    ]
start_time = time.time()


# Load the provided JSON data from the uploaded file
file_path = 'testfile.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract all image IDs from the geojson data
for feature in data['features']:
    image_id = feature['properties']['imageid']
    properties = feature['properties']
    directory_path = os.path.join("data", image_id)

    # Check if directory already exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory created: {directory_path}")
    else:
        print(f"Directory already exists: {directory_path}")
    # Define the path for the JSON file that will store the properties
    properties_file_path = os.path.join(directory_path, f"{image_id}_properties.json")

    # Write properties to a JSON file
    with open(properties_file_path, 'w', encoding='utf-8') as file:
        json.dump(properties, file, indent=4)
        print(f"Properties written to: {properties_file_path}")

    process_image_set(image_id, level, headers, schema, directory_path)

end_time = time.time()
duration = end_time - start_time
print(f"Total run duration: {duration} seconds")