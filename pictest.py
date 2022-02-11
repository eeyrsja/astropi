from PIL import Image
from numpy import array, logical_and, percentile, clip


i = 300

piccy = f"E:/ASTRO/zz_astropi_1_photo_{i}.jpg"

def get_cloud_percent(photo):
    """
    This function opens a photo and tries to estimate how much of the picture is covered by cloud.

    :param photo: the filename of the photo
    :return: the percentage of cloud cover in the photo
    """
    #logger.info(f"Function: get_cloud_percent") #TODO uncomment

    #open the image
    image = Image.open(photo)

    # rotate the picture - we think it is upside down?!
    image = image.rotate(180)

    # Crop the photo to remove the window frame
    width = image.size[0]
    height = image.size[1]
    image = image.crop((width * 0.15, height * 0.15, width * 0.85, height * 0.85))

    # Convert from R,G,B colour to H,S,V
    # WWe want to find clouds which have low "S"aturation and high "V"alue (or brightness)
    image_hsv = array(image.convert("HSV"))

    # Get the Saturation and Brightness parts
    saturation = image_hsv[:,:,1] / 255  # saturation is how colourful the pixel is - clouds are not colourful so saturation is low
    brightness = image_hsv[:, :, 2] / 255 # brightness of clouds is high

    # Increase the photo contrast - make the whites whiter and the blacks blacker
    # this is copied from https://stackoverflow.com/questions/48406578/adjusting-contrast-of-image-purely-with-numpy
    minval = percentile(brightness, 5)
    maxval = percentile(brightness, 95)
    brightness = clip(brightness, minval, maxval)
    brightness = ((brightness - minval) / (maxval - minval))

    # Apply threshold - if the number is less than saturation threshold AND more than brightness threshold then we treat it as cloud
    clouds = (saturation < 0.3) & (brightness > 0.5)

    # Work out the percentage cloud cover
    cloud_pixel_count = clouds.sum()
    total_pixel_count = clouds.size
    cloud_percent = 100.0 * cloud_pixel_count / total_pixel_count

    return cloud_percent


print(get_cloud_percent(piccy))


"""
piccy2 = piccy.rotate(180)
#piccy2.show()

crop = 400

left = 0 + crop
top = 0 + crop
bottom = 1944 - crop
right = 2592 - crop

piccy3 = piccy2.crop((left, top, right, bottom))

piccy4 = piccy3.convert('HSV')
piccy4.show()
piccy4 = array(piccy4)

piccy_h = piccy4[:,:,0]
piccy_s = piccy4[:,:,1]
piccy_v = piccy4[:,:,2]

Image.fromarray(piccy_v).show()



if False:
    minval = percentile(piccy4, 10)
    maxval = percentile(piccy4, 90)
    piccy4 = clip(piccy4, minval, maxval)
    piccy4 = ((piccy4 - minval) / (maxval - minval))
else:
    piccy4 = piccy4 / 255
Image.fromarray(piccy4 * 255).show()

piccy5 = piccy4 > 0.5
white_pixels = piccy5.sum()
total_pixels = piccy5.size
percentage_cloud = 100 * (white_pixels / total_pixels)
print(f"photo_{i}:  {percentage_cloud:0.2f}")

Image.fromarray(piccy5*255).show()
"""