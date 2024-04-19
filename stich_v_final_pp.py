import os
import requests
from PIL import Image
from io import BytesIO
import creds
import json
from multiprocessing import Pool
import time


def fetch_and_save_image(image_info):
    """Fetch an image from a URL and save it."""
    image_id, level, schema, directory_path = image_info
    base_url = "https://atlascbs360yeni.ibb.gov.tr"
    headers = {
        'Authorization': f'Basic {creds.api_key_2023}'
    }
    sides = ['R', 'B', 'U', 'D', 'L', 'F']
    for side in sides:
        for row, col in schema:
            url = f"{base_url}/panoramatiles/Tile/{image_id}/{level}/{side}/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_23.4.0"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                output_filename = f"{directory_path}/{image_id}_raw_{side}.jpg"
                image.save(output_filename)
            else:
                print(f"Failed to retrieve image from {url}. Status code: {response.status_code}")


def main():
    level = 2

    schema = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2)
    ]

    # Load the provided JSON data from the uploaded file
    file_path = 'testfile.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    image_info_list = []

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
        image_info_list.append((image_id, level, schema, directory_path))

    start_time = time.time()
    # Use multiprocessing Pool to parallelize image processing
    with Pool() as pool:
        pool.map(fetch_and_save_image, image_info_list)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Total run duration: {duration} seconds")


if __name__ == "__main__":
    main()
