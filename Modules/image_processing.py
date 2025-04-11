from PIL import Image, ImageChops

def is_pixel_black_or_white(pixel, threshold=30):
    red, green, blue = pixel
    average = (red + green + blue) / 3
    return 1 if average >= threshold else 0

def compute_difference(image1_path, image2_path, output_path):
    image_1 = Image.open(image1_path)
    image_2 = Image.open(image2_path)
    result = ImageChops.difference(image_1, image_2)
    result.save(output_path)
    return result
