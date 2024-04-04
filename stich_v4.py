import requests
from PIL import Image
from io import BytesIO
import creds


def fetch_and_open_image(url, headers):
    """Fetch an image from a URL and return it as an open PIL Image object."""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Failed to retrieve image from {url}. Status code: {response.status_code}")
        return None


def stitch_images(images, schema, output_filename):
    """Stitch together a list of images according to a schema and save the result."""
    stitched_image = Image.new('RGB', (len(set(x[0] for x in schema)) * 512, len(set(x[1] for x in schema)) * 512))
    for index, (row, col) in enumerate(schema):
        if images[index]:
            stitched_image.paste(images[index], (col * 512, row * 512))
    stitched_image.save(output_filename)


def process_image_set(image_name, level, headers, schema, stitch_schema):
    """Process a set of images for both raw and lidar data."""
    sides = ['R', 'B', 'U', 'D', 'L', 'F']
    base_url = "https://streetsmartcbs360.ibb.gov.tr/atlas"

    for side in sides:
        images_raw = []
        images_lidar = []
        for row, col in schema:
            url_raw = f"{base_url}/panoramatiles/Tile/{image_name}/{level}/{side}/{row}/{col}?apiKey={headers['Authorization'].split(' ')[1]}&nameVersion=streetsmart_18.4.0"
            url_lidar = f"{base_url}/depthtiles/{image_name}_{level}_{side}_{row}_{col}.png?apiKey={headers['Authorization'].split(' ')[1]}&nameVersion=streetsmart_18.4.0"

            image_raw = fetch_and_open_image(url_raw, headers)
            image_lidar = fetch_and_open_image(url_lidar, headers)

            if image_raw: images_raw.append(image_raw)
            if image_lidar: images_lidar.append(image_lidar)

        output_filename_raw = f"data/{image_name}_stitched_raw_{side}.jpg"
        output_filename_lidar = f"data/{image_name}_stitched_lidar_{side}.jpg"

        stitch_images(images_raw, stitch_schema, output_filename_raw)
        stitch_images(images_lidar, stitch_schema, output_filename_lidar)

    stitch_final_images([image_name], ['B', 'L', 'F', 'R'])  # Stitch final images after processing all sides


def stitch_final_images(image_names, sides_order):
    final_width = 6144
    final_height = 1536
    for image_name in image_names:
        final_image = Image.new('RGB', (final_width, final_height))
        for index, side in enumerate(sides_order):
            filename = f"data/{image_name}_stitched_raw_{side}.jpg"
            try:
                image = Image.open(filename)
                # Resize image to fit final dimensions
                resized_image = image.resize((final_width // len(sides_order), final_height))
                final_image.paste(resized_image, (index * final_width // len(sides_order), 0))
            except FileNotFoundError:
                print(f"File {filename} not found.")
        final_image.save(f"data/{image_name}_final_stitched.jpg")


payload = {}
headers = {
    'Authorization': f'Basic {creds.api_key}'
}

image_names = ["WE0NXXN0"]
# image_names = ["WE06U77N"]
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

for image_name in image_names:
    process_image_set(image_name, level, headers, schema, stitch_schema)
