import requests
from PIL import Image
from io import BytesIO
import creds

payload = {}
headers = {
    'Authorization': f'Basic {creds.api_key}'
}

image_names = ["WE0NXXN0"]


level = 2
schema = []

if level == 1:
    schema = [
        (0, 0)
    ]
    stitch_schema = [
        (0, 0)
    ]

if level == 2:
    schema = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2)
    ]
    stitch_schema = [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2)
    ]



# view schema is R, B, U, D
for image_name in image_names:
    raw_images_R = []
    raw_images_B = []
    raw_images_U = []
    raw_images_D = []
    raw_images_L = []
    raw_images_F = []
    lidar_images_R = []
    lidar_images_B = []
    lidar_images_U = []
    lidar_images_D = []
    lidar_images_L = []
    lidar_images_F = []

    # Fetch raw and lidar images
    for row, col in schema:
        url_raw_R = f"https://streetsmartcbs360.ibb.gov.tr/atlas/panoramatiles//Tile/{image_name}/{level}/R/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_raw_B = f"https://streetsmartcbs360.ibb.gov.tr/atlas/panoramatiles//Tile/{image_name}/{level}/B/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_raw_U = f"https://streetsmartcbs360.ibb.gov.tr/atlas/panoramatiles//Tile/{image_name}/{level}/U/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_raw_D = f"https://streetsmartcbs360.ibb.gov.tr/atlas/panoramatiles//Tile/{image_name}/{level}/D/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_raw_L = f"https://streetsmartcbs360.ibb.gov.tr/atlas/panoramatiles//Tile/{image_name}/{level}/L/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_raw_F = f"https://streetsmartcbs360.ibb.gov.tr/atlas/panoramatiles//Tile/{image_name}/{level}/F/{row}/{col}?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_lidar_R = f"https://streetsmartcbs360.ibb.gov.tr/atlas/depthtiles/{image_name}_{level}_R_{row}_{col}.png?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_lidar_B = f"https://streetsmartcbs360.ibb.gov.tr/atlas/depthtiles/{image_name}_{level}_B_{row}_{col}.png?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_lidar_U = f"https://streetsmartcbs360.ibb.gov.tr/atlas/depthtiles/{image_name}_{level}_U_{row}_{col}.png?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_lidar_D = f"https://streetsmartcbs360.ibb.gov.tr/atlas/depthtiles/{image_name}_{level}_D_{row}_{col}.png?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_lidar_L = f"https://streetsmartcbs360.ibb.gov.tr/atlas/depthtiles/{image_name}_{level}_L_{row}_{col}.png?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"
        url_lidar_F = f"https://streetsmartcbs360.ibb.gov.tr/atlas/depthtiles/{image_name}_{level}_F_{row}_{col}.png?apiKey=aXURmz8N2HUp-jsZu781q7Q1-noBeDElaPIxuXYJOn01OP4JmX8F6nkxSTElKr4h&nameVersion=streetsmart_18.4.0"

        response_raw_R = requests.request("GET", url_raw_R, headers=headers, data=payload)
        response_lidar_R = requests.request("GET", url_lidar_R, headers=headers, data=payload)
        response_raw_B = requests.request("GET", url_raw_B, headers=headers, data=payload)
        response_lidar_B = requests.request("GET", url_lidar_B, headers=headers, data=payload)
        response_raw_U = requests.request("GET", url_raw_U, headers=headers, data=payload)
        response_lidar_U = requests.request("GET", url_lidar_U, headers=headers, data=payload)
        response_raw_D = requests.request("GET", url_raw_D, headers=headers, data=payload)
        response_lidar_D = requests.request("GET", url_lidar_D, headers=headers, data=payload)
        response_raw_L = requests.request("GET", url_raw_L, headers=headers, data=payload)
        response_lidar_L = requests.request("GET", url_lidar_L, headers=headers, data=payload)
        response_raw_F = requests.request("GET", url_raw_F, headers=headers, data=payload)
        response_lidar_F = requests.request("GET", url_lidar_F, headers=headers, data=payload)

        if response_raw_R.status_code == 200 and response_lidar_R.status_code == 200:
            raw_images_R.append(Image.open(BytesIO(response_raw_R.content)))
            lidar_images_R.append(Image.open(BytesIO(response_lidar_R.content)))
            raw_images_B.append(Image.open(BytesIO(response_raw_B.content)))
            lidar_images_B.append(Image.open(BytesIO(response_lidar_B.content)))
            raw_images_U.append(Image.open(BytesIO(response_raw_U.content)))
            lidar_images_U.append(Image.open(BytesIO(response_lidar_U.content)))
            raw_images_D.append(Image.open(BytesIO(response_raw_D.content)))
            lidar_images_D.append(Image.open(BytesIO(response_lidar_D.content)))
            raw_images_L.append(Image.open(BytesIO(response_raw_L.content)))
            lidar_images_L.append(Image.open(BytesIO(response_lidar_L.content)))
            raw_images_F.append(Image.open(BytesIO(response_raw_F.content)))
            lidar_images_F.append(Image.open(BytesIO(response_lidar_F.content)))
        else:
            print(f"Failed to retrieve the image at ({row},{col}). Status code:", response_raw_R.status_code)

    # Stitch images based on stitch schema for raw images
    stitched_raw_image = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_raw_image.paste(raw_images_R[index], (col * 512, row * 512))

    # Save the stitched raw image
    stitched_raw_image.save(f"data/{image_name}_stitched_raw_R.jpg")

    # Stitch images based on stitch schema for lidar images
    stitched_lidar_image = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_lidar_image.paste(lidar_images_R[index], (col * 512, row * 512))

    # Save the stitched lidar image
    stitched_lidar_image.save(f"data/{image_name}_stitched_lidar_R.jpg")

    # Stitch images based on stitch schema for raw images
    stitched_raw_image_B = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_raw_image_B.paste(raw_images_B[index], (col * 512, row * 512))

    # Save the stitched raw image
    stitched_raw_image_B.save(f"data/{image_name}_stitched_raw_B.jpg")

    # Stitch images based on stitch schema for lidar images
    stitched_lidar_image_B = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_lidar_image_B.paste(lidar_images_B[index], (col * 512, row * 512))

    # Save the stitched lidar image
    stitched_lidar_image_B.save(f"data/{image_name}_stitched_lidar_B.jpg")

    # Stitch images based on stitch schema for raw images
    stitched_raw_image_U = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_raw_image_U.paste(raw_images_U[index], (col * 512, row * 512))

    # Save the stitched raw image
    stitched_raw_image_U.save(f"data/{image_name}_stitched_raw_U.jpg")

    # Stitch images based on stitch schema for lidar images
    stitched_lidar_image_U = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_lidar_image_U.paste(lidar_images_U[index], (col * 512, row * 512))

    # Save the stitched lidar image
    stitched_lidar_image_U.save(f"data/{image_name}_stitched_lidar_U.jpg")

    # Stitch images based on stitch schema for raw images
    stitched_raw_image_D = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_raw_image_D.paste(raw_images_D[index], (col * 512, row * 512))

    # Save the stitched raw image
    stitched_raw_image_D.save(f"data/{image_name}_stitched_raw_D.jpg")

    # Stitch images based on stitch schema for lidar images
    stitched_lidar_image_D = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_lidar_image_D.paste(lidar_images_D[index], (col * 512, row * 512))

    # Save the stitched lidar image
    stitched_lidar_image_D.save(f"data/{image_name}_stitched_lidar_D.jpg")

    # Stitch images based on stitch schema for raw images
    stitched_raw_image_L = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_raw_image_L.paste(raw_images_L[index], (col * 512, row * 512))

    # Save the stitched raw image
    stitched_raw_image_L.save(f"data/{image_name}_stitched_raw_L.jpg")

    # Stitch images based on stitch schema for lidar images
    stitched_lidar_image_L = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_lidar_image_L.paste(lidar_images_L[index], (col * 512, row * 512))

    # Save the stitched lidar image
    stitched_lidar_image_L.save(f"data/{image_name}_stitched_lidar_L.jpg")

    # Stitch images based on stitch schema for raw images
    stitched_raw_image_F = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_raw_image_F.paste(raw_images_F[index], (col * 512, row * 512))

    # Save the stitched raw image
    stitched_raw_image_F.save(f"data/{image_name}_stitched_raw_F.jpg")

    # Stitch images based on stitch schema for lidar images
    stitched_lidar_image_F = Image.new('RGB', (3 * 512, 3 * 512))
    for index, (row, col) in enumerate(stitch_schema):
        stitched_lidar_image_F.paste(lidar_images_F[index], (col * 512, row * 512))

    # Save the stitched lidar image
    stitched_lidar_image_F.save(f"data/{image_name}_stitched_lidar_F.jpg")
