from picamera import PiCamera
from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path
from time import sleep

base_folder = Path(__file__).parent.resolve()
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html

# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html


# Set up the camera
camera = PiCamera()
camera.resolution = (1296, 972)


photo_file = base_folder/'photo.jpg'
camera.start_preview(alpha=192)
sleep(.1) # Camera warm-up time
camera.capture(str(photo_file))
camera.stop_preview()

#Open image using Image module
im = Image.open(str(photo_file))
#Show actual Image
im.show()
#Show rotated Image
im = im.rotate(30)
im2 = im.transpose(Image.FLIP_LEFT_RIGHT)
im = im.filter(ImageFilter.DETAIL)
r, g, b = im.split()
im = Image.merge("RGB", (r, g, r))
im.show()
