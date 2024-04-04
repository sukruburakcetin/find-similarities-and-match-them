from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from PIL import Image
import requests


def fetch_image(url, headers):
    """Fetch an image and return the content."""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BytesIO(response.content)
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


def process_image_set_concurrently(image_name, level, headers, schema, stitch_schema):
    """Process a set of images for both raw and lidar data using concurrent requests."""
    sides = ['R', 'B', 'U', 'D', 'L', 'F']
    base_url = "https://streetsmartcbs360.ibb.gov.tr/atlas"

    with ThreadPoolExecutor(max_workers=20) as executor:
        for side in sides:
            future_to_url = {}
            for row, col in schema:
                url_raw = f"{base_url}/panoramatiles/Tile/{image_name}/{level}/{side}/{row}/{col}?apiKey={headers['Authorization'].split(' ')[1]}&nameVersion=streetsmart_18.4.0"
                url_lidar = f"{base_url}/depthtiles/{image_name}_{level}_{side}_{row}_{col}.png?apiKey={headers['Authorization'].split(' ')[1]}&nameVersion=streetsmart_18.4.0"

                future_to_url[executor.submit(fetch_image, url_raw, headers)] = ('raw', row, col)
                future_to_url[executor.submit(fetch_image, url_lidar, headers)] = ('lidar', row, col)

            images_raw = [None] * len(schema)
            images_lidar = [None] * len(schema)

            for future in as_completed(future_to_url):
                image_type, row, col = future_to_url[future]
                result = future.result()
                if result:
                    image = Image.open(result)
                    index = schema.index((row, col))
                    if image_type == 'raw':
                        images_raw[index] = image
                    else:
                        images_lidar[index] = image

            output_filename_raw = f"data/{image_name}_stitched_raw_{side}.jpg"
            output_filename_lidar = f"data/{image_name}_stitched_lidar_{side}.jpg"

            stitch_images(images_raw, stitch_schema, output_filename_raw)
            stitch_images(images_lidar, stitch_schema, output_filename_lidar)
