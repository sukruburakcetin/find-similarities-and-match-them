import requests
from PIL import Image
from io import BytesIO
import creds

payload = {}

headers = {
    'Authorization': f'Basic {creds.api_key_2023}'
}

image_names = ["WE0NXXN0"]

level = 2

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

        url_raw_L = f"https://atlascbs360yeni.ibb.gov.tr/panoramatiles//Tile/{image_name}/{level}/L/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h & nameVersion =streetsmart_23.4.0"
        url_raw_R = f"https://atlascbs360yeni.ibb.gov.tr/panoramatiles//Tile/{image_name}/{level}/R/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h & nameVersion =streetsmart_23.4.0"
        url_raw_B = f"https://atlascbs360yeni.ibb.gov.tr/panoramatiles//Tile/{image_name}/{level}/B/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h & nameVersion =streetsmart_23.4.0"
        url_raw_F = f"https://atlascbs360yeni.ibb.gov.tr/panoramatiles//Tile/{image_name}/{level}/F/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h & nameVersion =streetsmart_23.4.0"
        url_raw_U = f"https://atlascbs360yeni.ibb.gov.tr/panoramatiles//Tile/{image_name}/{level}/U/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h & nameVersion =streetsmart_23.4.0"

        response_raw_L = requests.request("GET", url_raw_L, headers=headers, data=payload)
        response_raw_R = requests.request("GET", url_raw_R, headers=headers, data=payload)
        response_raw_B = requests.request("GET", url_raw_B, headers=headers, data=payload)
        response_raw_F = requests.request("GET", url_raw_F, headers=headers, data=payload)
        response_raw_U = requests.request("GET", url_raw_U, headers=headers, data=payload)

        # Check if the request was successful
        if response_raw_L.status_code == 200:
            # Read the image from the response
            image_data_raw_L = BytesIO(response_raw_L.content)
            image_data_raw_R = BytesIO(response_raw_R.content)
            image_data_raw_B = BytesIO(response_raw_B.content)
            image_data_raw_F = BytesIO(response_raw_F.content)
            image_data_raw_U = BytesIO(response_raw_U.content)

            # Open the image using PIL
            image_raw_L = Image.open(image_data_raw_L)
            image_raw_R = Image.open(image_data_raw_R)
            image_raw_B = Image.open(image_data_raw_B)
            image_raw_F = Image.open(image_data_raw_F)
            image_raw_U = Image.open(image_data_raw_U)

            # Save the image
            image_raw_L.save(f"data/{image_name}_raw_L_{row}_{col}.jpg")  # Save with appropriate name
            image_raw_R.save(f"data/{image_name}_raw_R_{row}_{col}.jpg")  # Save with appropriate name
            image_raw_B.save(f"data/{image_name}_raw_B_{row}_{col}.jpg")  # Save with appropriate name
            image_raw_F.save(f"data/{image_name}_raw_F_{row}_{col}.jpg")  # Save with appropriate name
            image_raw_U.save(f"data/{image_name}_raw_U_{row}_{col}.jpg")  # Save with appropriate name

            # Display the image
            # image_raw.show()
            # image_lidar.show()
        else:
            print(f"Failed to retrieve the response_raw at ({row},{col}). Status code:", response_raw_L.status_code)
    print(f"Process is done on {image_name}.")
