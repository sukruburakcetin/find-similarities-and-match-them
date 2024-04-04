import requests
from PIL import Image
from io import BytesIO
import creds
import cv2
import numpy as np


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

        # Load the final stitched image
        panoramic_img = cv2.imread(f"data/{image_name}_final_stitched.jpg")
        fisheye_img = panoramic_to_fisheye(panoramic_img)  # Convert the final stitched image to fisheye

        # Save fisheye image
        cv2.imwrite(f"data/{image_name}_final_fish_eye.jpg", fisheye_img)  # Save the fisheye image
        print("Fisheye image saved successfully!")  # Print a success message


def panoramic_to_fisheye(panoramic_image):
    # Extract the height and width of the panoramic image
    panoramic_height, panoramic_width = panoramic_image.shape[:2]

    # Calculate the dimensions of the fisheye image
    fisheye_height = min(panoramic_height, panoramic_width)  # Set height to be minimum of width and height
    fisheye_width = fisheye_height * 2  # Set width to be twice the height to maintain 2:1 aspect ratio

    # Initialize an empty array to store the fisheye image
    fisheye_image = np.zeros((fisheye_height, fisheye_width, 3), dtype=np.uint8)

    # Calculate fisheye parameters
    center_x = fisheye_width // 2  # Calculate the x-coordinate of the center
    center_y = fisheye_height // 2  # Calculate the y-coordinate of the center
    radius = min(center_x, center_y)  # Calculate the radius of the circular fisheye region

    # Create a binary mask to identify the circular region of interest in the fisheye image
    mask = np.zeros((fisheye_height, fisheye_width), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 255, -1)  # Draw a filled circle on the mask

    # Convert panoramic image to fisheye
    for y in range(fisheye_height):
        for x in range(fisheye_width):
            if mask[y, x] == 255:  # Check if the pixel falls within the circular region of interest
                # Calculate polar coordinates
                theta = np.arctan2(y - center_y, x - center_x)  # Angle relative to the center
                rho = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)  # Distance from the center

                # Map polar coordinates to equirectangular coordinates of the panoramic image
                panoramic_x = int((theta / np.pi + 1) * (panoramic_width / 2))  # Map angle to width
                panoramic_y = int((rho / radius) * panoramic_height)  # Map distance to height

                # Handle edge cases where the mapped coordinates may exceed the bounds of the panoramic image
                if panoramic_x >= panoramic_width:
                    panoramic_x = panoramic_width - 1
                if panoramic_y >= panoramic_height:
                    panoramic_y = panoramic_height - 1

                # Copy pixel value from panoramic image to fisheye image
                fisheye_image[y, x] = panoramic_image[panoramic_y, panoramic_x]

    return fisheye_image


# Example usage
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
