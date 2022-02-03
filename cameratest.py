from picamera import PiCamera
from PIL import Image

# https://picamera.readthedocs.io/en/release-1.13/recipes1.html

# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html


# Set up the camera
camera = PiCamera()
camera.resolution = (1296, 972)

base_folder = Path(__file__).parent.resolve()

photo_file = base_folder/'photo.jpg'
camera.start_preview()
sleep(2) # Camera warm-up time
camera.capture(photo_file)

#Open image using Image module
im = Image.open(base_folder/'photo.jpg')
#Show actual Image
im.show()
#Show rotated Image
im = im.rotate(45)
im.show()