import requests
from PIL import Image
from io import BytesIO
import creds

payload = {}

headers = {
    'Authorization': f'Basic {creds.api_key_2023}'
}

image_names = ["WE0NXXN0"]

level = 1

if level == 1:
    schema = [
        (0, 0)
    ]
if level == 2:
    schema = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2)
    ]

for image_name in image_names:
    for row, col in schema:
        # url_raw = f"https://streetsmartcbs360.ibb.gov.tr/atlas/panoramatiles//Tile/{image_name}/{level}/R/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        # url_lidar = f"https://streetsmartcbs360.ibb.gov.tr/atlas/depthtiles/{image_name}_{level}_R_{row}_{col}.png?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"

        url_raw = f"https://atlascbs360yeni.ibb.gov.tr/panoramatiles//Tile/{image_name}/{level}/L/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h & nameVersion =streetsmart_23.4.0"

        response_raw = requests.request("GET", url_raw, headers=headers, data=payload)

        # Check if the request was successful
        if response_raw.status_code == 200:
            # Read the image from the response
            image_data_raw = BytesIO(response_raw.content)

            # Open the image using PIL
            image_raw = Image.open(image_data_raw)

            # Save the image
            image_raw.save(f"data/{image_name}_raw_{row}_{col}.jpg")  # Save with appropriate name

            # Display the image
            # image_raw.show()
            # image_lidar.show()
        else:
            print(f"Failed to retrieve the response_raw at ({row},{col}). Status code:", response_raw.status_code)
    print(f"Process is done on {image_name}.")
